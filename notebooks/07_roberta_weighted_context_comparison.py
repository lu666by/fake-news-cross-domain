from __future__ import annotations

import copy
import gc
import random
import re
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

# Current weighted RoBERTa reference from the finished seed sweep.
WEIGHTED_ROBERTA_SINGLE_ACC = 0.6606156274664562
WEIGHTED_ROBERTA_SINGLE_MACRO_F1 = 0.6495641501957979
WEIGHTED_ROBERTA_SINGLE_REAL_RECALL = 0.7436974789915967
WEIGHTED_ROBERTA_SINGLE_FAKE_RECALL = 0.5533453887884268

DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")


def set_seed(seed: int) -> None:
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)
        torch.backends.cudnn.deterministic = True
        torch.backends.cudnn.benchmark = False


def clean_series(series: pd.Series) -> pd.Series:
    return series.fillna("").astype(str).str.replace(r"\s+", " ", regex=True).str.strip()


def build_input_series(df: pd.DataFrame, variant: str) -> pd.Series:
    statement = clean_series(df["statement"])

    if variant == "statement_only":
        return statement

    if variant == "statement_plus_context":
        context = clean_series(df["context"])
        has_context = context != ""
        out = statement.copy()
        out.loc[has_context] = statement.loc[has_context] + " [CTX] " + context.loc[has_context]
        return out

    raise ValueError(f"Unknown variant: {variant}")


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


def make_dataloader(texts, labels, tokenizer, batch_size: int, shuffle: bool) -> DataLoader:
    dataset = EncodedTextDataset(texts, labels, tokenizer, MAX_LENGTH)
    return DataLoader(
        dataset,
        batch_size=batch_size,
        shuffle=shuffle,
        num_workers=0,
        pin_memory=torch.cuda.is_available(),
    )


def move_batch_to_device(batch, device):
    return {key: value.to(device) for key, value in batch.items()}


def train_one_epoch(model, dataloader, optimizer, scheduler, device, class_weights):
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


def evaluate_with_probs(model, dataloader, device):
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
    return metrics


def run_variant(
    variant: str,
    train_p: pd.DataFrame,
    valid_p: pd.DataFrame,
    test_p: pd.DataFrame,
    class_weights: torch.Tensor,
    context_mask: pd.Series,
) -> dict:
    print()
    print(f"===== Running variant: {variant} =====")

    set_seed(RANDOM_SEED)

    train_texts = build_input_series(train_p, variant)
    valid_texts = build_input_series(valid_p, variant)
    test_texts = build_input_series(test_p, variant)

    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
    model = AutoModelForSequenceClassification.from_pretrained(
        MODEL_NAME,
        num_labels=2,
        id2label=ID2LABEL,
        label2id={label_name: label_id for label_id, label_name in ID2LABEL.items()},
    )
    model.to(DEVICE)

    train_loader = make_dataloader(train_texts.tolist(), train_p["y"].tolist(), tokenizer, TRAIN_BATCH_SIZE, True)
    valid_loader = make_dataloader(valid_texts.tolist(), valid_p["y"].tolist(), tokenizer, EVAL_BATCH_SIZE, False)
    test_loader = make_dataloader(test_texts.tolist(), test_p["y"].tolist(), tokenizer, EVAL_BATCH_SIZE, False)

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

    started = time.perf_counter()

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

        print(f"{variant} epoch {epoch}/{NUM_EPOCHS}{checkpoint_note}")
        print(f"  elapsed: {time.perf_counter() - epoch_started:.2f}s")
        print(
            f"  train: loss={train_metrics['loss']:.4f}, "
            f"acc={train_metrics['accuracy']:.4f}, "
            f"macro_f1={train_metrics['macro_f1']:.4f}"
        )
        print(
            f"  valid: loss={valid_metrics['loss']:.4f}, "
            f"acc={valid_metrics['accuracy']:.4f}, "
            f"macro_f1={valid_metrics['macro_f1']:.4f}"
        )

    if best_state_dict is None:
        raise RuntimeError(f"No checkpoint for variant {variant}")

    model.load_state_dict(best_state_dict)
    print(f"Loaded best_state_dict into model for {variant} from epoch {best_epoch} before test evaluation.")

    best_valid_metrics = evaluate_with_probs(model, valid_loader, DEVICE)
    test_metrics = evaluate_with_probs(model, test_loader, DEVICE)

    cm = test_metrics["confusion_matrix"]
    real_recall = cm[0, 0] / cm[0].sum()
    fake_recall = cm[1, 1] / cm[1].sum()

    context_gold = test_p.loc[context_mask, "y"].to_numpy()
    context_preds = test_metrics["preds"][context_mask.to_numpy()]
    context_metrics = evaluate_predictions(context_gold, context_preds)
    context_errors = int((context_preds != context_gold).sum())

    total_minutes = (time.perf_counter() - started) / 60.0
    print(f"{variant} total run time: {total_minutes:.2f} minutes")

    result = {
        "variant": variant,
        "best_epoch": best_epoch,
        "valid_accuracy": best_valid_metrics["accuracy"],
        "valid_macro_f1": best_valid_metrics["macro_f1"],
        "test_accuracy": test_metrics["accuracy"],
        "test_macro_f1": test_metrics["macro_f1"],
        "real_recall": real_recall,
        "fake_recall": fake_recall,
        "confusion_matrix": cm.tolist(),
        "context_dep_count": int(context_mask.sum()),
        "context_dep_accuracy": context_metrics["accuracy"],
        "context_dep_macro_f1": context_metrics["macro_f1"],
        "context_dep_errors": context_errors,
        "test_preds": test_metrics["preds"],
        "test_probs": test_metrics["probs"],
        "training_minutes": total_minutes,
    }

    del tokenizer, model, train_loader, valid_loader, test_loader, optimizer, scheduler
    gc.collect()
    torch.cuda.empty_cache()
    return result


def prepare_example_table(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty:
        return pd.DataFrame([{"note": "No examples for this section."}])

    out = df[
        [
            "statement",
            "context",
            "gold_label",
            "statement_only_label",
            "statement_only_prob_fake",
            "statement_plus_context_label",
            "statement_plus_context_prob_fake",
        ]
    ].copy()
    out["statement_only_prob_fake"] = out["statement_only_prob_fake"].map(lambda x: f"{x:.4f}")
    out["statement_plus_context_prob_fake"] = out["statement_plus_context_prob_fake"].map(lambda x: f"{x:.4f}")
    return out


def main() -> None:
    if not torch.cuda.is_available():
        raise RuntimeError("CUDA is required for this controlled RoBERTa context experiment.")

    print("Parameters:")
    print("  DATA_DIR =", DATA_DIR)
    print("  MODEL_NAME =", MODEL_NAME)
    print("  MAX_LENGTH =", MAX_LENGTH)
    print("  TRAIN_BATCH_SIZE =", TRAIN_BATCH_SIZE)
    print("  EVAL_BATCH_SIZE =", EVAL_BATCH_SIZE)
    print("  NUM_EPOCHS =", NUM_EPOCHS)
    print("  LEARNING_RATE =", LEARNING_RATE)
    print("  WEIGHT_DECAY =", WEIGHT_DECAY)
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
    print()
    print("Class weights:")
    for class_id, class_name in ID2LABEL.items():
        print(f"  {class_name} ({class_id}): {class_weights[class_id].item():.4f}")

    context_re = re.compile(r"\b(this|that|these|those|he|she|they|it|his|her|their|here|there)\b", re.I)
    context_mask = test_p["statement"].fillna("").astype(str).apply(lambda s: bool(context_re.search(s)))

    statement_only_result = run_variant(
        "statement_only",
        train_p=train_p,
        valid_p=valid_p,
        test_p=test_p,
        class_weights=class_weights,
        context_mask=context_mask,
    )
    statement_plus_context_result = run_variant(
        "statement_plus_context",
        train_p=train_p,
        valid_p=valid_p,
        test_p=test_p,
        class_weights=class_weights,
        context_mask=context_mask,
    )

    comparison_df = pd.DataFrame(
        [
            {key: value for key, value in statement_only_result.items() if key not in {"test_preds", "test_probs"}},
            {key: value for key, value in statement_plus_context_result.items() if key not in {"test_preds", "test_probs"}},
        ]
    )

    analysis_df = test_p.reset_index(drop=True).copy()
    analysis_df["context_dependent"] = context_mask.to_numpy()
    analysis_df["gold_label"] = analysis_df["y"].map(ID2LABEL)
    analysis_df["statement_only_pred"] = statement_only_result["test_preds"]
    analysis_df["statement_only_label"] = analysis_df["statement_only_pred"].map(ID2LABEL)
    analysis_df["statement_only_prob_fake"] = statement_only_result["test_probs"][:, 1]
    analysis_df["statement_plus_context_pred"] = statement_plus_context_result["test_preds"]
    analysis_df["statement_plus_context_label"] = analysis_df["statement_plus_context_pred"].map(ID2LABEL)
    analysis_df["statement_plus_context_prob_fake"] = statement_plus_context_result["test_probs"][:, 1]

    improved_context = analysis_df[
        (analysis_df["context_dependent"])
        & (analysis_df["statement_only_pred"] != analysis_df["y"])
        & (analysis_df["statement_plus_context_pred"] == analysis_df["y"])
    ].copy()
    regressed_context = analysis_df[
        (analysis_df["context_dependent"])
        & (analysis_df["statement_only_pred"] == analysis_df["y"])
        & (analysis_df["statement_plus_context_pred"] != analysis_df["y"])
    ].copy()

    improved_context = improved_context.sort_values("statement_plus_context_prob_fake", ascending=False).head(10)
    regressed_context = regressed_context.sort_values("statement_plus_context_prob_fake", ascending=False).head(10)

    improved_context_table = prepare_example_table(improved_context)
    regressed_context_table = prepare_example_table(regressed_context)

    print()
    print("Overall comparison:")
    print(
        comparison_df[
            [
                "variant",
                "best_epoch",
                "valid_accuracy",
                "valid_macro_f1",
                "test_accuracy",
                "test_macro_f1",
                "real_recall",
                "fake_recall",
                "context_dep_accuracy",
                "context_dep_macro_f1",
                "context_dep_errors",
                "training_minutes",
            ]
        ]
    )

    md_lines = []
    md_lines.append("# Weighted RoBERTa Statement vs Context Comparison")
    md_lines.append("")
    md_lines.append(f"- Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    md_lines.append("- Model: `roberta-base` with weighted training loss")
    md_lines.append("- Seed: `52`")
    md_lines.append("- Controlled change: input text only")
    md_lines.append("- Variant A: `statement` only")
    md_lines.append('- Variant B: `statement + " [CTX] " + context`')
    md_lines.append("")

    export_df = comparison_df.copy()
    for col in [
        "valid_accuracy",
        "valid_macro_f1",
        "test_accuracy",
        "test_macro_f1",
        "real_recall",
        "fake_recall",
        "context_dep_accuracy",
        "context_dep_macro_f1",
        "training_minutes",
    ]:
        export_df[col] = export_df[col].map(lambda x: f"{x:.4f}")

    md_lines.append("## Overall Comparison")
    md_lines.append("")
    md_lines.append(
        dataframe_to_markdown(
            export_df[
                [
                    "variant",
                    "best_epoch",
                    "valid_accuracy",
                    "valid_macro_f1",
                    "test_accuracy",
                    "test_macro_f1",
                    "real_recall",
                    "fake_recall",
                    "context_dep_accuracy",
                    "context_dep_macro_f1",
                    "context_dep_errors",
                    "training_minutes",
                ]
            ]
        )
    )
    md_lines.append("")
    md_lines.append("## Interpretation")
    md_lines.append("")

    if statement_plus_context_result["context_dep_errors"] < statement_only_result["context_dep_errors"]:
        md_lines.append("- Adding context reduced context-dependent errors in this controlled comparison.")
    elif statement_plus_context_result["context_dep_errors"] > statement_only_result["context_dep_errors"]:
        md_lines.append("- Adding context increased context-dependent errors in this controlled comparison.")
    else:
        md_lines.append("- Adding context did not change the number of context-dependent errors in this controlled comparison.")

    md_lines.append(
        f"- Context-dependent subset size: `{statement_only_result['context_dep_count']}`"
    )
    md_lines.append(
        f"- Statement-only context-dependent accuracy: `{statement_only_result['context_dep_accuracy']:.4f}`"
    )
    md_lines.append(
        f"- Statement+context context-dependent accuracy: `{statement_plus_context_result['context_dep_accuracy']:.4f}`"
    )
    md_lines.append(
        f"- Statement-only context-dependent macro-F1: `{statement_only_result['context_dep_macro_f1']:.4f}`"
    )
    md_lines.append(
        f"- Statement+context context-dependent macro-F1: `{statement_plus_context_result['context_dep_macro_f1']:.4f}`"
    )
    md_lines.append(
        f"- Statement-only context-dependent errors: `{statement_only_result['context_dep_errors']}`"
    )
    md_lines.append(
        f"- Statement+context context-dependent errors: `{statement_plus_context_result['context_dep_errors']}`"
    )
    md_lines.append("")
    md_lines.append("## Direct Comparison vs Current Weighted RoBERTa Baseline")
    md_lines.append("")
    md_lines.append(
        f"- Current weighted RoBERTa baseline (seed 52, statement only reference): "
        f"Accuracy `{WEIGHTED_ROBERTA_SINGLE_ACC:.4f}`, Macro-F1 `{WEIGHTED_ROBERTA_SINGLE_MACRO_F1:.4f}`, "
        f"REAL recall `{WEIGHTED_ROBERTA_SINGLE_REAL_RECALL:.4f}`, FAKE recall `{WEIGHTED_ROBERTA_SINGLE_FAKE_RECALL:.4f}`"
    )
    md_lines.append(
        f"- Statement-only rerun: Accuracy `{statement_only_result['test_accuracy']:.4f}`, "
        f"Macro-F1 `{statement_only_result['test_macro_f1']:.4f}`, "
        f"REAL recall `{statement_only_result['real_recall']:.4f}`, "
        f"FAKE recall `{statement_only_result['fake_recall']:.4f}`"
    )
    md_lines.append(
        f"- Statement+context: Accuracy `{statement_plus_context_result['test_accuracy']:.4f}`, "
        f"Macro-F1 `{statement_plus_context_result['test_macro_f1']:.4f}`, "
        f"REAL recall `{statement_plus_context_result['real_recall']:.4f}`, "
        f"FAKE recall `{statement_plus_context_result['fake_recall']:.4f}`"
    )
    md_lines.append("")
    md_lines.append("## Context-Dependent Cases Improved By Adding Context")
    md_lines.append("")
    md_lines.append(dataframe_to_markdown(improved_context_table))
    md_lines.append("")
    md_lines.append("## Context-Dependent Cases Hurt By Adding Context")
    md_lines.append("")
    md_lines.append(dataframe_to_markdown(regressed_context_table))

    out_dir = Path("results")
    out_dir.mkdir(parents=True, exist_ok=True)
    md_path = out_dir / "roberta_weighted_statement_vs_context_comparison.md"
    csv_path = out_dir / "roberta_weighted_statement_vs_context_comparison.csv"
    md_path.write_text("\n".join(md_lines), encoding="utf-8")
    comparison_df.to_csv(csv_path, index=False)

    print()
    print("Saved markdown:", md_path.resolve())
    print("Saved csv:", csv_path.resolve())


if __name__ == "__main__":
    main()
