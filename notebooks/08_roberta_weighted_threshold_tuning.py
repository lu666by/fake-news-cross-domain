from __future__ import annotations

import copy
import gc
import random
import time
from datetime import datetime
from pathlib import Path

import numpy as np
import pandas as pd
import torch
import torch.nn.functional as F
from torch.optim import AdamW
from torch.utils.data import DataLoader, Dataset
from transformers import AutoModelForSequenceClassification, AutoTokenizer, get_linear_schedule_with_warmup

from liar_utils import ID2LABEL, dataframe_to_markdown, evaluate_predictions, load_binary_dataset_splits, make_liar_config


DATA_DIR = Path("liar_dataset")
MODEL_NAME = "roberta-base"
MAX_LENGTH = 128
TRAIN_BATCH_SIZE = 16
EVAL_BATCH_SIZE = 32
NUM_EPOCHS = 3
LEARNING_RATE = 2e-5
WEIGHT_DECAY = 0.01
WARMUP_RATIO = 0.1
RANDOM_SEED = 52
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")


def set_seed(seed: int) -> None:
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)
        torch.backends.cudnn.deterministic = True
        torch.backends.cudnn.benchmark = False


class EncodedTextDataset(Dataset):
    def __init__(self, texts, labels, tokenizer, max_length: int):
        self.encodings = tokenizer(
            list(texts),
            truncation=True,
            padding="max_length",
            max_length=max_length,
            return_tensors="pt",
        )
        self.labels = torch.tensor(list(labels), dtype=torch.long)

    def __len__(self) -> int:
        return len(self.labels)

    def __getitem__(self, idx: int) -> dict:
        item = {key: value[idx] for key, value in self.encodings.items()}
        item["labels"] = self.labels[idx]
        return item


def make_dataloader(df: pd.DataFrame, tokenizer, text_column: str, batch_size: int, shuffle: bool) -> DataLoader:
    dataset = EncodedTextDataset(
        texts=df[text_column].tolist(),
        labels=df["y"].tolist(),
        tokenizer=tokenizer,
        max_length=MAX_LENGTH,
    )
    return DataLoader(
        dataset,
        batch_size=batch_size,
        shuffle=shuffle,
        num_workers=0,
        pin_memory=torch.cuda.is_available(),
    )


def move_batch_to_device(batch: dict, device: torch.device) -> dict:
    return {key: value.to(device) for key, value in batch.items()}


def train_one_epoch(model, dataloader, optimizer, scheduler, device: torch.device, class_weights: torch.Tensor) -> dict:
    model.train()
    total_loss = 0.0
    all_labels = []
    all_preds = []

    for batch in dataloader:
        batch = move_batch_to_device(batch, device)
        optimizer.zero_grad()

        labels = batch["labels"]
        model_inputs = {key: value for key, value in batch.items() if key != "labels"}
        outputs = model(**model_inputs)
        loss = F.cross_entropy(outputs.logits, labels, weight=class_weights)
        loss.backward()

        torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)
        optimizer.step()
        scheduler.step()

        total_loss += loss.item()

        preds = outputs.logits.detach().cpu().argmax(dim=1)
        all_preds.extend(preds.tolist())
        all_labels.extend(labels.detach().cpu().tolist())

    metrics = evaluate_predictions(all_labels, all_preds)
    metrics["loss"] = total_loss / max(len(dataloader), 1)
    return metrics


def evaluate_with_probs(model, dataloader, device: torch.device) -> dict:
    model.eval()
    total_loss = 0.0
    all_labels = []
    all_preds = []
    all_probs = []

    with torch.inference_mode():
        for batch in dataloader:
            batch = move_batch_to_device(batch, device)
            outputs = model(**batch)
            total_loss += outputs.loss.item()

            probs = torch.softmax(outputs.logits, dim=1).detach().cpu().numpy()
            preds = probs.argmax(axis=1)
            labels = batch["labels"].detach().cpu().numpy()

            all_probs.append(probs)
            all_preds.extend(preds.tolist())
            all_labels.extend(labels.tolist())

    all_probs = np.vstack(all_probs)
    metrics = evaluate_predictions(all_labels, all_preds)
    metrics["loss"] = total_loss / max(len(dataloader), 1)
    metrics["preds"] = np.array(all_preds)
    metrics["probs"] = all_probs
    metrics["labels"] = np.array(all_labels)
    return metrics


def apply_threshold(prob_fake: np.ndarray, threshold: float) -> np.ndarray:
    return (prob_fake >= threshold).astype(int)


def summarise_threshold(y_true: np.ndarray, prob_fake: np.ndarray, threshold: float) -> dict:
    preds = apply_threshold(prob_fake, threshold)
    metrics = evaluate_predictions(y_true, preds)
    cm = metrics["confusion_matrix"]
    real_recall = cm[0, 0] / cm[0].sum()
    fake_recall = cm[1, 1] / cm[1].sum()
    return {
        "threshold": threshold,
        "accuracy": metrics["accuracy"],
        "macro_f1": metrics["macro_f1"],
        "real_recall": real_recall,
        "fake_recall": fake_recall,
        "confusion_matrix": cm.tolist(),
        "preds": preds,
    }


def main() -> None:
    if not torch.cuda.is_available():
        raise RuntimeError("CUDA is required for this weighted RoBERTa threshold experiment.")

    print("Parameters:")
    print("  DATA_DIR =", DATA_DIR)
    print("  MODEL_NAME =", MODEL_NAME)
    print("  MAX_LENGTH =", MAX_LENGTH)
    print("  TRAIN_BATCH_SIZE =", TRAIN_BATCH_SIZE)
    print("  EVAL_BATCH_SIZE =", EVAL_BATCH_SIZE)
    print("  NUM_EPOCHS =", NUM_EPOCHS)
    print("  RANDOM_SEED =", RANDOM_SEED)
    print("  DEVICE =", DEVICE)

    set_seed(RANDOM_SEED)

    dataset_config = make_liar_config(DATA_DIR)
    train_p, valid_p, test_p = load_binary_dataset_splits(dataset_config)

    train_counts = train_p["y"].value_counts().sort_index()
    num_classes = len(ID2LABEL)
    num_train = len(train_p)
    class_weights = torch.tensor(
        [num_train / (num_classes * train_counts.loc[class_id]) for class_id in sorted(ID2LABEL)],
        dtype=torch.float,
        device=DEVICE,
    )

    print("Prepared shapes:")
    print("  train_p:", train_p.shape)
    print("  valid_p:", valid_p.shape)
    print("  test_p :", test_p.shape)
    print("Class weights:")
    for class_id, class_name in ID2LABEL.items():
        print(f"  {class_name} ({class_id}): {class_weights[class_id].item():.4f}")

    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
    model = AutoModelForSequenceClassification.from_pretrained(
        MODEL_NAME,
        num_labels=2,
        id2label=ID2LABEL,
        label2id={label_name: label_id for label_id, label_name in ID2LABEL.items()},
    )
    model.to(DEVICE)

    train_loader = make_dataloader(train_p, tokenizer, dataset_config.text_column, TRAIN_BATCH_SIZE, True)
    valid_loader = make_dataloader(valid_p, tokenizer, dataset_config.text_column, EVAL_BATCH_SIZE, False)
    test_loader = make_dataloader(test_p, tokenizer, dataset_config.text_column, EVAL_BATCH_SIZE, False)

    optimizer = AdamW(model.parameters(), lr=LEARNING_RATE, weight_decay=WEIGHT_DECAY)
    total_training_steps = len(train_loader) * NUM_EPOCHS
    warmup_steps = int(total_training_steps * WARMUP_RATIO)
    scheduler = get_linear_schedule_with_warmup(
        optimizer,
        num_warmup_steps=warmup_steps,
        num_training_steps=total_training_steps,
    )

    best_state_dict = None
    best_epoch = None
    best_valid_score = (-1.0, -1.0)
    training_started = time.perf_counter()

    for epoch in range(1, NUM_EPOCHS + 1):
        epoch_started = time.perf_counter()
        train_metrics = train_one_epoch(model, train_loader, optimizer, scheduler, DEVICE, class_weights)
        valid_metrics = evaluate_with_probs(model, valid_loader, DEVICE)
        current_valid_score = (valid_metrics["macro_f1"], valid_metrics["accuracy"])

        if current_valid_score > best_valid_score:
            best_valid_score = current_valid_score
            best_epoch = epoch
            best_state_dict = copy.deepcopy(model.state_dict())
            checkpoint_note = " <- saved best checkpoint"
        else:
            checkpoint_note = ""

        print(f"epoch {epoch}/{NUM_EPOCHS}{checkpoint_note}")
        print(f"  elapsed: {time.perf_counter() - epoch_started:.2f}s")
        print(
            f"  train: loss={train_metrics['loss']:.4f}, "
            f"acc={train_metrics['accuracy']:.4f}, "
            f"macro_f1={train_metrics['macro_f1']:.4f}"
        )
        print(
            f"  valid @0.5: loss={valid_metrics['loss']:.4f}, "
            f"acc={valid_metrics['accuracy']:.4f}, "
            f"macro_f1={valid_metrics['macro_f1']:.4f}"
        )

    if best_state_dict is None:
        raise RuntimeError("No best checkpoint was captured.")

    model.load_state_dict(best_state_dict)
    print(f"Loaded best_state_dict into model from epoch {best_epoch} before threshold tuning and test evaluation.")

    valid_eval = evaluate_with_probs(model, valid_loader, DEVICE)
    test_eval = evaluate_with_probs(model, test_loader, DEVICE)
    valid_prob_fake = valid_eval["probs"][:, 1]
    test_prob_fake = test_eval["probs"][:, 1]

    thresholds = np.round(np.arange(0.30, 0.701, 0.01), 2)
    threshold_rows = []
    best_threshold_summary = None
    best_threshold_score = (-1.0, -1.0, -1.0)

    for threshold in thresholds:
        valid_summary = summarise_threshold(valid_eval["labels"], valid_prob_fake, float(threshold))
        threshold_rows.append(
            {
                "threshold": threshold,
                "valid_accuracy": valid_summary["accuracy"],
                "valid_macro_f1": valid_summary["macro_f1"],
                "valid_real_recall": valid_summary["real_recall"],
                "valid_fake_recall": valid_summary["fake_recall"],
                "valid_confusion_matrix": valid_summary["confusion_matrix"],
            }
        )

        current_score = (
            valid_summary["macro_f1"],
            valid_summary["accuracy"],
            valid_summary["fake_recall"],
        )
        if current_score > best_threshold_score:
            best_threshold_score = current_score
            best_threshold_summary = valid_summary

    if best_threshold_summary is None:
        raise RuntimeError("Threshold tuning did not produce a best threshold.")

    default_valid = summarise_threshold(valid_eval["labels"], valid_prob_fake, 0.50)
    default_test = summarise_threshold(test_eval["labels"], test_prob_fake, 0.50)
    tuned_test = summarise_threshold(test_eval["labels"], test_prob_fake, best_threshold_summary["threshold"])

    run_minutes = (time.perf_counter() - training_started) / 60.0
    print()
    print("Threshold tuning summary:")
    print(
        f"  best threshold on valid = {best_threshold_summary['threshold']:.2f} "
        f"(macro_f1={best_threshold_summary['macro_f1']:.4f}, "
        f"acc={best_threshold_summary['accuracy']:.4f}, "
        f"fake_recall={best_threshold_summary['fake_recall']:.4f})"
    )
    print(
        f"  default test @0.50: acc={default_test['accuracy']:.4f}, "
        f"macro_f1={default_test['macro_f1']:.4f}, "
        f"real_recall={default_test['real_recall']:.4f}, "
        f"fake_recall={default_test['fake_recall']:.4f}"
    )
    print(
        f"  tuned test @{best_threshold_summary['threshold']:.2f}: acc={tuned_test['accuracy']:.4f}, "
        f"macro_f1={tuned_test['macro_f1']:.4f}, "
        f"real_recall={tuned_test['real_recall']:.4f}, "
        f"fake_recall={tuned_test['fake_recall']:.4f}"
    )
    print(f"  total run time: {run_minutes:.2f} minutes")

    out_dir = Path("results")
    out_dir.mkdir(parents=True, exist_ok=True)

    threshold_df = pd.DataFrame(threshold_rows)
    threshold_df.to_csv(out_dir / "roberta_weighted_threshold_scan_seed52.csv", index=False)

    comparison_df = pd.DataFrame(
        [
            {
                "setting": "default_0.50",
                "threshold": 0.50,
                "best_epoch": best_epoch,
                "valid_accuracy": default_valid["accuracy"],
                "valid_macro_f1": default_valid["macro_f1"],
                "valid_real_recall": default_valid["real_recall"],
                "valid_fake_recall": default_valid["fake_recall"],
                "test_accuracy": default_test["accuracy"],
                "test_macro_f1": default_test["macro_f1"],
                "test_real_recall": default_test["real_recall"],
                "test_fake_recall": default_test["fake_recall"],
                "test_confusion_matrix": default_test["confusion_matrix"],
            },
            {
                "setting": "tuned_threshold",
                "threshold": best_threshold_summary["threshold"],
                "best_epoch": best_epoch,
                "valid_accuracy": best_threshold_summary["accuracy"],
                "valid_macro_f1": best_threshold_summary["macro_f1"],
                "valid_real_recall": best_threshold_summary["real_recall"],
                "valid_fake_recall": best_threshold_summary["fake_recall"],
                "test_accuracy": tuned_test["accuracy"],
                "test_macro_f1": tuned_test["macro_f1"],
                "test_real_recall": tuned_test["real_recall"],
                "test_fake_recall": tuned_test["fake_recall"],
                "test_confusion_matrix": tuned_test["confusion_matrix"],
            },
        ]
    )
    comparison_df.to_csv(out_dir / "roberta_weighted_threshold_comparison_seed52.csv", index=False)

    export_df = comparison_df.copy()
    for col in [
        "threshold",
        "valid_accuracy",
        "valid_macro_f1",
        "valid_real_recall",
        "valid_fake_recall",
        "test_accuracy",
        "test_macro_f1",
        "test_real_recall",
        "test_fake_recall",
    ]:
        export_df[col] = export_df[col].map(lambda x: f"{x:.4f}")

    top_thresholds_df = threshold_df.sort_values(
        ["valid_macro_f1", "valid_accuracy", "valid_fake_recall"],
        ascending=[False, False, False],
    ).head(10).copy()
    for col in ["threshold", "valid_accuracy", "valid_macro_f1", "valid_real_recall", "valid_fake_recall"]:
        top_thresholds_df[col] = top_thresholds_df[col].map(lambda x: f"{x:.4f}")

    md_lines = []
    md_lines.append("# Weighted RoBERTa Threshold Tuning (Seed 52)")
    md_lines.append("")
    md_lines.append(f"- Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    md_lines.append("- Model: `roberta-base` with weighted training loss")
    md_lines.append("- Input: `statement` only")
    md_lines.append("- Seed: `52`")
    md_lines.append("- Thresholds scanned on validation: `0.30` to `0.70` in steps of `0.01`")
    md_lines.append("- Best checkpoint still selected by validation macro-F1 at the default argmax classifier stage")
    md_lines.append("- Threshold tuning is applied only after loading `best_state_dict`")
    md_lines.append("")
    md_lines.append("## Comparison")
    md_lines.append("")
    md_lines.append(dataframe_to_markdown(export_df))
    md_lines.append("")
    md_lines.append("## Top Validation Thresholds")
    md_lines.append("")
    md_lines.append(dataframe_to_markdown(top_thresholds_df))
    md_lines.append("")
    md_lines.append("## Interpretation")
    md_lines.append("")

    fake_recall_delta = tuned_test["fake_recall"] - default_test["fake_recall"]
    accuracy_delta = tuned_test["accuracy"] - default_test["accuracy"]
    macro_f1_delta = tuned_test["macro_f1"] - default_test["macro_f1"]
    real_recall_delta = tuned_test["real_recall"] - default_test["real_recall"]

    if best_threshold_summary["threshold"] < 0.50:
        boundary_note = "The tuned threshold is lower than 0.50, so it makes the model less conservative about predicting FAKE."
    elif best_threshold_summary["threshold"] > 0.50:
        boundary_note = "The tuned threshold is higher than 0.50, so it makes the model more conservative about predicting FAKE."
    else:
        boundary_note = "The tuned threshold stayed at 0.50, so validation did not support moving the FAKE decision boundary."

    md_lines.append(f"- Best validation threshold: `{best_threshold_summary['threshold']:.2f}`")
    md_lines.append(boundary_note)
    md_lines.append(f"- Test accuracy change vs 0.50: `{accuracy_delta:+.4f}`")
    md_lines.append(f"- Test macro-F1 change vs 0.50: `{macro_f1_delta:+.4f}`")
    md_lines.append(f"- Test REAL recall change vs 0.50: `{real_recall_delta:+.4f}`")
    md_lines.append(f"- Test FAKE recall change vs 0.50: `{fake_recall_delta:+.4f}`")

    md_path = out_dir / "roberta_weighted_threshold_tuning_seed52.md"
    md_path.write_text("\n".join(md_lines), encoding="utf-8")

    print("Saved threshold scan csv:", (out_dir / "roberta_weighted_threshold_scan_seed52.csv").resolve())
    print("Saved comparison csv:", (out_dir / "roberta_weighted_threshold_comparison_seed52.csv").resolve())
    print("Saved markdown:", md_path.resolve())

    del tokenizer, model, train_loader, valid_loader, test_loader, optimizer, scheduler
    gc.collect()
    torch.cuda.empty_cache()


if __name__ == "__main__":
    main()
