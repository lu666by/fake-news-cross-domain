from __future__ import annotations

import argparse
import copy
import importlib.util
import time
from datetime import datetime
from pathlib import Path

import pandas as pd
import torch
import torch.nn.functional as F
from sklearn.metrics import recall_score
from sklearn.model_selection import train_test_split
from torch.optim import AdamW
from transformers import AutoModelForSequenceClassification, AutoTokenizer, get_linear_schedule_with_warmup

from cross_dataset_utils import find_project_root, format_float, load_fakenewsnet_minimal
from liar_utils import ID2LABEL, dataframe_to_markdown, evaluate_predictions, load_binary_dataset_splits, make_liar_config


PROJECT_ROOT = find_project_root()
SOURCE_SCRIPT = PROJECT_ROOT / "notebooks" / "10_cross_dataset_transformer_liar_to_fakenewsnet.py"
RESULTS_DIR = PROJECT_ROOT / "results" / "intermediate_finetuning"

spec = importlib.util.spec_from_file_location("cross_transformer", SOURCE_SCRIPT)
cross_transformer = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(cross_transformer)

EncodedTextDataset = cross_transformer.EncodedTextDataset
MODEL_PRESETS = cross_transformer.MODEL_PRESETS
make_dataloader = cross_transformer.make_dataloader
move_batch_to_device = cross_transformer.move_batch_to_device
set_seed = cross_transformer.set_seed


def compute_class_weights(df: pd.DataFrame, device: torch.device) -> torch.Tensor:
    counts = df["y"].value_counts().sort_index()
    total = len(df)
    num_classes = len(ID2LABEL)
    return torch.tensor(
        [total / (num_classes * counts.loc[class_id]) for class_id in sorted(ID2LABEL)],
        dtype=torch.float,
        device=device,
    )


def train_epoch(model, dataloader, optimizer, scheduler, device: torch.device, class_weights: torch.Tensor | None) -> dict:
    model.train()
    total_loss = 0.0
    labels_all = []
    preds_all = []
    for batch in dataloader:
        batch = move_batch_to_device(batch, device)
        optimizer.zero_grad(set_to_none=True)
        labels = batch["labels"]
        inputs = {key: value for key, value in batch.items() if key != "labels"}
        outputs = model(**inputs)
        loss = F.cross_entropy(outputs.logits, labels, weight=class_weights)
        loss.backward()
        torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)
        optimizer.step()
        scheduler.step()

        total_loss += loss.item()
        labels_all.extend(labels.detach().cpu().tolist())
        preds_all.extend(outputs.logits.detach().cpu().argmax(dim=1).tolist())

    metrics = evaluate_predictions(labels_all, preds_all)
    metrics["loss"] = total_loss / max(len(dataloader), 1)
    return metrics


def evaluate_model(model, dataloader, device: torch.device) -> dict:
    model.eval()
    total_loss = 0.0
    labels_all = []
    preds_all = []
    with torch.inference_mode():
        for batch in dataloader:
            batch = move_batch_to_device(batch, device)
            outputs = model(**batch)
            total_loss += outputs.loss.item()
            labels_all.extend(batch["labels"].detach().cpu().tolist())
            preds_all.extend(outputs.logits.detach().cpu().argmax(dim=1).tolist())

    metrics = evaluate_predictions(labels_all, preds_all)
    metrics["loss"] = total_loss / max(len(dataloader), 1)
    metrics["labels"] = labels_all
    metrics["preds"] = preds_all
    return metrics


def metric_row(seed: int, model_key: str, stage: str, target_train_n: int, target_fraction: float, best_epoch: int, metrics: dict, elapsed: float) -> dict:
    real_recall, fake_recall = recall_score(
        metrics["labels"],
        metrics["preds"],
        labels=[0, 1],
        average=None,
        zero_division=0,
    )
    return {
        "seed": seed,
        "model_key": model_key,
        "stage": stage,
        "target_fraction": target_fraction,
        "target_train_n": target_train_n,
        "best_epoch": best_epoch,
        "test_n": len(metrics["labels"]),
        "accuracy": metrics["accuracy"],
        "macro_f1": metrics["macro_f1"],
        "real_recall": real_recall,
        "fake_recall": fake_recall,
        "confusion_matrix": metrics["confusion_matrix"].tolist(),
        "classification_report": metrics["classification_report"],
        "elapsed_minutes": elapsed,
    }


def split_fakenewsnet(fnn: pd.DataFrame, seed: int, test_size: float, valid_size: float) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    train_valid, test = train_test_split(
        fnn,
        test_size=test_size,
        random_state=seed,
        stratify=fnn["y"],
    )
    train, valid = train_test_split(
        train_valid,
        test_size=valid_size,
        random_state=seed,
        stratify=train_valid["y"],
    )
    return train.reset_index(drop=True), valid.reset_index(drop=True), test.reset_index(drop=True)


def sample_balanced_fraction(df: pd.DataFrame, fraction: float, seed: int) -> pd.DataFrame:
    groups = []
    for _, group in df.groupby("y", sort=False):
        n = max(1, int(round(len(group) * fraction)))
        groups.append(group.sample(n=min(n, len(group)), random_state=seed))
    return pd.concat(groups, ignore_index=True).sample(frac=1.0, random_state=seed).reset_index(drop=True)


def train_with_best_checkpoint(
    model,
    train_df: pd.DataFrame,
    valid_df: pd.DataFrame,
    text_column: str,
    tokenizer,
    device: torch.device,
    args,
    epochs: int,
    learning_rate: float,
    batch_size: int,
    class_weights: torch.Tensor | None,
    stage_name: str,
) -> tuple[dict, int, list[dict]]:
    train_loader = make_dataloader(train_df, text_column, tokenizer, args.max_length, batch_size, shuffle=True)
    valid_loader = make_dataloader(valid_df, text_column, tokenizer, args.max_length, args.eval_batch_size, shuffle=False)

    optimizer = AdamW(model.parameters(), lr=learning_rate, weight_decay=args.weight_decay)
    total_steps = len(train_loader) * epochs
    scheduler = get_linear_schedule_with_warmup(
        optimizer,
        num_warmup_steps=int(total_steps * args.warmup_ratio),
        num_training_steps=total_steps,
    )

    best_state = None
    best_epoch = 0
    best_score = (-1.0, -1.0)
    history = []
    for epoch in range(1, epochs + 1):
        epoch_start = time.time()
        train_metrics = train_epoch(model, train_loader, optimizer, scheduler, device, class_weights)
        valid_metrics = evaluate_model(model, valid_loader, device)
        score = (valid_metrics["macro_f1"], valid_metrics["accuracy"])
        if score > best_score:
            best_score = score
            best_epoch = epoch
            best_state = copy.deepcopy(model.state_dict())
            note = " <- best"
        else:
            note = ""
        history.append(
            {
                "stage": stage_name,
                "epoch": epoch,
                "train_loss": train_metrics["loss"],
                "train_accuracy": train_metrics["accuracy"],
                "train_macro_f1": train_metrics["macro_f1"],
                "valid_loss": valid_metrics["loss"],
                "valid_accuracy": valid_metrics["accuracy"],
                "valid_macro_f1": valid_metrics["macro_f1"],
                "elapsed_minutes": (time.time() - epoch_start) / 60,
            }
        )
        print(
            f"{stage_name} epoch {epoch}/{epochs}{note} | "
            f"train macro_f1={train_metrics['macro_f1']:.4f} | valid macro_f1={valid_metrics['macro_f1']:.4f}",
            flush=True,
        )

    if best_state is None:
        raise RuntimeError(f"No best checkpoint for {stage_name}")
    model.load_state_dict(best_state)
    return best_state, best_epoch, history


def compact_table(df: pd.DataFrame) -> pd.DataFrame:
    cols = [
        "model_key",
        "seed",
        "stage",
        "target_fraction",
        "target_train_n",
        "test_n",
        "accuracy",
        "macro_f1",
        "real_recall",
        "fake_recall",
        "confusion_matrix",
    ]
    out = df[cols].copy()
    for col in ["target_fraction", "accuracy", "macro_f1", "real_recall", "fake_recall"]:
        out[col] = out[col].map(format_float)
    return out


def save_outputs(results: list[dict], history: list[dict], args) -> None:
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    results_df = pd.DataFrame(results)
    history_df = pd.DataFrame(history)
    compact = compact_table(results_df)
    fraction_suffix = args.target_fractions.replace(",", "_").replace(".", "p")
    suffix = f"{args.model_key}_seeds_{args.seeds.replace(',', '_')}_fractions_{fraction_suffix}"

    results_df.to_csv(RESULTS_DIR / f"intermediate_finetuning_{suffix}_full.csv", index=False)
    compact.to_csv(RESULTS_DIR / f"intermediate_finetuning_{suffix}_compact.csv", index=False)
    history_df.to_csv(RESULTS_DIR / f"intermediate_finetuning_{suffix}_history.csv", index=False)

    lines = [
        "# Intermediate Fine-Tuning: LIAR -> FakeNewsNet",
        "",
        f"- Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}",
        f"- Model key: `{args.model_key}`",
        f"- Seeds: `{args.seeds}`",
        "- Source stage: train on LIAR train, select checkpoint by LIAR validation Macro-F1.",
        "- Intermediate stage: continue fine-tuning on a stratified target fraction of FakeNewsNet train titles, select checkpoint by FakeNewsNet validation Macro-F1.",
        "- Final target evaluation: held-out FakeNewsNet test titles.",
        "- This is the main follow-up experiment after the direct LIAR -> FakeNewsNet transfer baseline.",
        "",
        "## Compact Results",
        "",
        dataframe_to_markdown(compact),
        "",
        "## Interpretation Guide",
        "",
        "- `source_only_zero_shot` is the original LIAR-trained model evaluated directly on FakeNewsNet test.",
        "- `intermediate_ft` rows show whether small target-domain supervision improves FakeNewsNet performance.",
        "- Compare Macro-F1, REAL recall, and FAKE recall together; high FAKE recall with very low REAL recall indicates a biased transfer model.",
        "",
    ]
    (RESULTS_DIR / f"intermediate_finetuning_{suffix}.md").write_text("\n".join(lines), encoding="utf-8")
    print(f"Saved intermediate fine-tuning outputs to {RESULTS_DIR}", flush=True)


def run(args) -> None:
    if args.model_key not in MODEL_PRESETS:
        raise ValueError(f"Unknown model key: {args.model_key}")

    preset = MODEL_PRESETS[args.model_key]
    model_name = args.model_name or preset["model_name"]
    seeds = [int(seed.strip()) for seed in args.seeds.split(",") if seed.strip()]
    fractions = [float(value.strip()) for value in args.target_fractions.split(",") if value.strip()]

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print("Device:", device, flush=True)
    if device.type == "cuda":
        print("GPU:", torch.cuda.get_device_name(0), flush=True)
    elif args.require_cuda:
        raise RuntimeError("CUDA is required but unavailable.")

    liar_config = make_liar_config(PROJECT_ROOT / "data" / "liar_dataset")
    liar_train, liar_valid, _ = load_binary_dataset_splits(liar_config)
    fnn = load_fakenewsnet_minimal(PROJECT_ROOT / "data" / "fakenewsnet_minimal" / "raw")
    tokenizer = AutoTokenizer.from_pretrained(model_name)

    all_results = []
    all_history = []
    for seed in seeds:
        print(f"\n=== Seed {seed} ===", flush=True)
        set_seed(seed)
        fnn_train, fnn_valid, fnn_test = split_fakenewsnet(fnn, seed, args.target_test_size, args.target_valid_size)
        print(f"FakeNewsNet split sizes: train={len(fnn_train)}, valid={len(fnn_valid)}, test={len(fnn_test)}", flush=True)

        source_start = time.time()
        model = AutoModelForSequenceClassification.from_pretrained(
            model_name,
            num_labels=2,
            id2label=ID2LABEL,
            label2id={label_name: label_id for label_id, label_name in ID2LABEL.items()},
        )
        model.to(device)

        source_weights = compute_class_weights(liar_train, device) if preset.get("use_class_weights", True) else None
        source_state, source_best_epoch, source_history = train_with_best_checkpoint(
            model,
            liar_train,
            liar_valid,
            liar_config.text_column,
            tokenizer,
            device,
            args,
            args.source_epochs,
            args.source_learning_rate,
            args.train_batch_size,
            source_weights,
            "source_liar",
        )
        for item in source_history:
            item.update({"seed": seed, "model_key": args.model_key, "target_fraction": 0.0, "target_train_n": 0})
        all_history.extend(source_history)

        fnn_test_loader = make_dataloader(fnn_test, "text", tokenizer, args.max_length, args.eval_batch_size, shuffle=False)
        zero_metrics = evaluate_model(model, fnn_test_loader, device)
        all_results.append(
            metric_row(
                seed,
                args.model_key,
                "source_only_zero_shot",
                0,
                0.0,
                source_best_epoch,
                zero_metrics,
                (time.time() - source_start) / 60,
            )
        )
        print(f"source_only_zero_shot FakeNewsNet test macro_f1={zero_metrics['macro_f1']:.4f}", flush=True)

        for fraction in fractions:
            ft_start = time.time()
            target_subset = sample_balanced_fraction(fnn_train, fraction, seed)
            print(f"\nIntermediate fine-tuning fraction={fraction:.4f}, target_train_n={len(target_subset)}", flush=True)

            ft_model = AutoModelForSequenceClassification.from_pretrained(
                model_name,
                num_labels=2,
                id2label=ID2LABEL,
                label2id={label_name: label_id for label_id, label_name in ID2LABEL.items()},
            )
            ft_model.load_state_dict(source_state)
            ft_model.to(device)
            target_weights = compute_class_weights(target_subset, device) if args.target_class_weights else None
            _, target_best_epoch, target_history = train_with_best_checkpoint(
                ft_model,
                target_subset,
                fnn_valid,
                "text",
                tokenizer,
                device,
                args,
                args.target_epochs,
                args.target_learning_rate,
                args.target_train_batch_size,
                target_weights,
                f"intermediate_ft_{fraction:.4f}",
            )
            for item in target_history:
                item.update({"seed": seed, "model_key": args.model_key, "target_fraction": fraction, "target_train_n": len(target_subset)})
            all_history.extend(target_history)

            ft_metrics = evaluate_model(ft_model, fnn_test_loader, device)
            all_results.append(
                metric_row(
                    seed,
                    args.model_key,
                    "intermediate_ft",
                    len(target_subset),
                    fraction,
                    target_best_epoch,
                    ft_metrics,
                    (time.time() - ft_start) / 60,
                )
            )
            print(
                f"intermediate_ft fraction={fraction:.4f}: "
                f"acc={ft_metrics['accuracy']:.4f}, macro_f1={ft_metrics['macro_f1']:.4f}",
                flush=True,
            )
            del ft_model
            if torch.cuda.is_available():
                torch.cuda.empty_cache()

        del model
        if torch.cuda.is_available():
            torch.cuda.empty_cache()

    save_outputs(all_results, all_history, args)


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--model-key", default="weighted_roberta", choices=sorted(MODEL_PRESETS))
    parser.add_argument("--model-name", default=None)
    parser.add_argument("--seeds", default="42")
    parser.add_argument("--target-fractions", default="0.01,0.05,0.10")
    parser.add_argument("--source-epochs", type=int, default=3)
    parser.add_argument("--target-epochs", type=int, default=2)
    parser.add_argument("--max-length", type=int, default=128)
    parser.add_argument("--train-batch-size", type=int, default=16)
    parser.add_argument("--target-train-batch-size", type=int, default=16)
    parser.add_argument("--eval-batch-size", type=int, default=64)
    parser.add_argument("--source-learning-rate", type=float, default=2e-5)
    parser.add_argument("--target-learning-rate", type=float, default=1e-5)
    parser.add_argument("--weight-decay", type=float, default=0.01)
    parser.add_argument("--warmup-ratio", type=float, default=0.1)
    parser.add_argument("--target-test-size", type=float, default=0.2)
    parser.add_argument("--target-valid-size", type=float, default=0.2)
    parser.add_argument("--target-class-weights", action="store_true")
    parser.add_argument("--require-cuda", action="store_true")
    return parser.parse_args()


if __name__ == "__main__":
    run(parse_args())
