from __future__ import annotations

import argparse
import copy
import random
import time
from datetime import datetime
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import torch
import torch.nn.functional as F
from sklearn.metrics import recall_score
from torch.optim import AdamW
from torch.utils.data import DataLoader, Dataset
from transformers import AutoModelForSequenceClassification, AutoTokenizer, get_linear_schedule_with_warmup

from cross_dataset_utils import find_project_root, format_float, load_fakenewsnet_minimal
from liar_utils import ID2LABEL, dataframe_to_markdown, evaluate_predictions, load_binary_dataset_splits, make_liar_config


MODEL_PRESETS = {
    "weighted_roberta": {
        "model_name": "roberta-base",
        "title": "Weighted RoBERTa",
        "use_class_weights": True,
    },
    "weighted_bert": {
        "model_name": "bert-base-uncased",
        "title": "Weighted BERT",
        "use_class_weights": True,
    },
    "unweighted_bert": {
        "model_name": "bert-base-uncased",
        "title": "Unweighted BERT",
        "use_class_weights": False,
    },
}


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


def set_seed(seed: int) -> None:
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)
        torch.backends.cudnn.deterministic = True
        torch.backends.cudnn.benchmark = False


def make_dataloader(df: pd.DataFrame, text_column: str, tokenizer, max_length: int, batch_size: int, shuffle: bool) -> DataLoader:
    dataset = EncodedTextDataset(
        texts=df[text_column].tolist(),
        labels=df["y"].tolist(),
        tokenizer=tokenizer,
        max_length=max_length,
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


def train_one_epoch(model, dataloader, optimizer, scheduler, device: torch.device, class_weights: torch.Tensor | None) -> dict:
    model.train()
    total_loss = 0.0
    all_labels = []
    all_preds = []

    for batch in dataloader:
        batch = move_batch_to_device(batch, device)
        optimizer.zero_grad(set_to_none=True)

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


def evaluate_model(model, dataloader, device: torch.device) -> dict:
    model.eval()
    total_loss = 0.0
    all_labels = []
    all_preds = []

    with torch.inference_mode():
        for batch in dataloader:
            batch = move_batch_to_device(batch, device)
            outputs = model(**batch)
            total_loss += outputs.loss.item()

            preds = outputs.logits.detach().cpu().argmax(dim=1)
            all_preds.extend(preds.tolist())
            all_labels.extend(batch["labels"].detach().cpu().tolist())

    metrics = evaluate_predictions(all_labels, all_preds)
    metrics["loss"] = total_loss / max(len(dataloader), 1)
    metrics["preds"] = all_preds
    metrics["labels"] = all_labels
    return metrics


def metric_row(seed: int, target: str, best_epoch: int, metrics: dict, elapsed_minutes: float) -> dict:
    real_recall, fake_recall = recall_score(
        metrics["labels"],
        metrics["preds"],
        labels=[0, 1],
        average=None,
        zero_division=0,
    )
    return {
        "seed": seed,
        "target": target,
        "best_epoch": best_epoch,
        "n": len(metrics["labels"]),
        "accuracy": metrics["accuracy"],
        "macro_f1": metrics["macro_f1"],
        "real_recall": real_recall,
        "fake_recall": fake_recall,
        "confusion_matrix": metrics["confusion_matrix"].tolist(),
        "classification_report": metrics["classification_report"],
        "elapsed_minutes": elapsed_minutes,
    }


def build_targets(liar_config, test_df: pd.DataFrame, fnn: pd.DataFrame) -> list[tuple[str, pd.DataFrame, str]]:
    return [
        ("LIAR test", test_df, liar_config.text_column),
        ("FakeNewsNet PolitiFact titles", fnn[fnn["source"] == "politifact"].copy(), "text"),
        ("FakeNewsNet GossipCop titles", fnn[fnn["source"] == "gossipcop"].copy(), "text"),
        ("FakeNewsNet combined titles", fnn.copy(), "text"),
    ]


def aggregate_results(results_df: pd.DataFrame) -> pd.DataFrame:
    metric_cols = ["accuracy", "macro_f1", "real_recall", "fake_recall"]
    rows = []
    for target, group in results_df.groupby("target", sort=False):
        row = {"target": target, "runs": len(group)}
        for metric in metric_cols:
            row[f"{metric}_mean"] = group[metric].mean()
            row[f"{metric}_std"] = group[metric].std(ddof=1) if len(group) > 1 else 0.0
        row["elapsed_minutes_mean"] = group["elapsed_minutes"].mean()
        rows.append(row)
    return pd.DataFrame(rows)


def make_compact_table(df: pd.DataFrame, aggregate: bool = False) -> pd.DataFrame:
    out = df.copy()
    float_cols = [col for col in out.columns if any(key in col for key in ["accuracy", "macro_f1", "real_recall", "fake_recall", "elapsed"])]
    for col in float_cols:
        out[col] = out[col].map(format_float)
    return out


def save_figures(results_df: pd.DataFrame, agg_df: pd.DataFrame, model_key: str, model_title: str, figures_dir: Path) -> None:
    figures_dir.mkdir(parents=True, exist_ok=True)
    sns.set_theme(style="whitegrid")

    plot_df = agg_df.melt(
        id_vars=["target"],
        value_vars=["accuracy_mean", "macro_f1_mean", "real_recall_mean", "fake_recall_mean"],
        var_name="metric",
        value_name="score",
    )
    plot_df["metric"] = plot_df["metric"].str.replace("_mean", "", regex=False).str.replace("_", " ").str.title()

    plt.figure(figsize=(12, 6))
    ax = sns.barplot(data=plot_df, x="target", y="score", hue="metric")
    ax.set_title(f"{model_title}: LIAR to FakeNewsNet Transfer Metrics")
    ax.set_xlabel("")
    ax.set_ylabel("Score")
    ax.set_ylim(0, 1)
    ax.tick_params(axis="x", rotation=20)
    plt.tight_layout()
    plt.savefig(figures_dir / f"{model_key}_cross_dataset_metrics.png", dpi=200)
    plt.close()

    # Confusion matrix for the combined target, aggregated across all seeds.
    combined = results_df[results_df["target"] == "FakeNewsNet combined titles"]
    if not combined.empty:
        cm_total = np.zeros((2, 2), dtype=int)
        for cm in combined["confusion_matrix"]:
            cm_total += np.array(cm)
        plt.figure(figsize=(5.8, 4.8))
        ax = sns.heatmap(
            cm_total,
            annot=True,
            fmt="d",
            cmap="Blues",
            xticklabels=["Pred REAL", "Pred FAKE"],
            yticklabels=["Gold REAL", "Gold FAKE"],
        )
        ax.set_title(f"{model_title}: FakeNewsNet Combined Confusion Matrix")
        plt.tight_layout()
        plt.savefig(figures_dir / f"{model_key}_fakenewsnet_combined_confusion_matrix.png", dpi=200)
        plt.close()


def save_report(
    model_key: str,
    model_title: str,
    model_name: str,
    seeds: list[int],
    results_df: pd.DataFrame,
    history_df: pd.DataFrame,
    out_dir: Path,
    figures_dir: Path,
    use_class_weights: bool = True,
) -> None:
    agg_df = aggregate_results(results_df)
    compact_results = make_compact_table(
        results_df[
            [
                "seed",
                "target",
                "best_epoch",
                "n",
                "accuracy",
                "macro_f1",
                "real_recall",
                "fake_recall",
                "confusion_matrix",
                "elapsed_minutes",
            ]
        ]
    )
    compact_agg = make_compact_table(agg_df)

    results_df.to_csv(out_dir / f"cross_dataset_{model_key}_liar_to_fakenewsnet_full.csv", index=False)
    compact_results.to_csv(out_dir / f"cross_dataset_{model_key}_liar_to_fakenewsnet.csv", index=False)
    compact_agg.to_csv(out_dir / f"cross_dataset_{model_key}_liar_to_fakenewsnet_summary.csv", index=False)
    history_df.to_csv(out_dir / f"cross_dataset_{model_key}_training_history.csv", index=False)

    save_figures(results_df, agg_df, model_key, model_title, figures_dir)

    lines = [
        f"# Cross-Dataset {model_title}: LIAR to FakeNewsNet Minimal",
        "",
        f"- Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}",
        f"- HuggingFace model: `{model_name}`",
        f"- Seeds: `{', '.join(map(str, seeds))}`",
        "- Source training data: LIAR train split",
        "- Checkpoint selection: LIAR validation Macro-F1",
        "- Test/evaluation targets: LIAR test, FakeNewsNet PolitiFact titles, FakeNewsNet GossipCop titles, FakeNewsNet combined titles",
        "- Class weights: " + ("computed from LIAR train split only for each run" if use_class_weights else "None (unweighted cross-entropy)"),
        "- Target data is never used for training or checkpoint selection",
        "",
        "## Aggregate Results",
        "",
        dataframe_to_markdown(compact_agg),
        "",
        "## Per-Run Results",
        "",
        dataframe_to_markdown(compact_results),
        "",
        "## Figures",
        "",
        f"- Metrics chart: `figures/{model_key}_cross_dataset_metrics.png`",
        f"- Combined confusion matrix: `figures/{model_key}_fakenewsnet_combined_confusion_matrix.png`",
        "",
        "## Thesis Interpretation",
        "",
        "This experiment tests whether a transformer model trained on LIAR transfers directly to FakeNewsNet minimal titles. Because FakeNewsNet minimal is title-only, the result should be described as LIAR statement to FakeNewsNet title transfer, not full-article fake news detection.",
        "",
    ]

    (out_dir / f"cross_dataset_{model_key}_liar_to_fakenewsnet.md").write_text("\n".join(lines), encoding="utf-8")


def run(args) -> None:
    if args.model_key not in MODEL_PRESETS:
        raise ValueError(f"Unknown model_key {args.model_key}. Choose from {sorted(MODEL_PRESETS)}")

    preset = MODEL_PRESETS[args.model_key]
    model_name = args.model_name or preset["model_name"]
    model_title = preset["title"] if args.model_title is None else args.model_title
    seeds = [int(seed.strip()) for seed in args.seeds.split(",") if seed.strip()]

    project_root = find_project_root()
    out_dir = project_root / "results" / "cross_dataset"
    figures_dir = out_dir / "figures"
    out_dir.mkdir(parents=True, exist_ok=True)
    figures_dir.mkdir(parents=True, exist_ok=True)

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print("Device:", device, flush=True)
    if device.type == "cuda":
        print("GPU:", torch.cuda.get_device_name(0), flush=True)
    elif args.require_cuda:
        raise RuntimeError("CUDA is required but torch.cuda.is_available() is False.")

    liar_config = make_liar_config(project_root / "data" / "liar_dataset")
    train_df, valid_df, test_df = load_binary_dataset_splits(liar_config)
    fnn = load_fakenewsnet_minimal(project_root / "data" / "fakenewsnet_minimal" / "raw")
    targets = build_targets(liar_config, test_df, fnn)

    tokenizer = AutoTokenizer.from_pretrained(model_name)

    all_rows = []
    history_rows = []

    for run_idx, seed in enumerate(seeds, start=1):
        seed_start = time.time()
        print(f"\n=== {model_title} seed {seed} ({run_idx}/{len(seeds)}) ===", flush=True)
        set_seed(seed)

        use_class_weights = preset.get("use_class_weights", True)
        if use_class_weights:
            train_counts = train_df["y"].value_counts().sort_index()
            num_train = len(train_df)
            num_classes = len(ID2LABEL)
            class_weights = torch.tensor(
                [num_train / (num_classes * train_counts.loc[class_id]) for class_id in sorted(ID2LABEL)],
                dtype=torch.float,
                device=device,
            )
            print("Class weights:", [round(x, 4) for x in class_weights.detach().cpu().tolist()], flush=True)
        else:
            class_weights = None
            print("Class weights: None (unweighted cross-entropy)", flush=True)

        model = AutoModelForSequenceClassification.from_pretrained(
            model_name,
            num_labels=2,
            id2label=ID2LABEL,
            label2id={label_name: label_id for label_id, label_name in ID2LABEL.items()},
        )
        model.to(device)

        train_loader = make_dataloader(train_df, liar_config.text_column, tokenizer, args.max_length, args.train_batch_size, shuffle=True)
        valid_loader = make_dataloader(valid_df, liar_config.text_column, tokenizer, args.max_length, args.eval_batch_size, shuffle=False)

        optimizer = AdamW(model.parameters(), lr=args.learning_rate, weight_decay=args.weight_decay)
        total_training_steps = len(train_loader) * args.epochs
        warmup_steps = int(total_training_steps * args.warmup_ratio)
        scheduler = get_linear_schedule_with_warmup(
            optimizer,
            num_warmup_steps=warmup_steps,
            num_training_steps=total_training_steps,
        )

        best_state_dict = None
        best_epoch = None
        best_valid_score = (-1.0, -1.0)

        for epoch in range(1, args.epochs + 1):
            epoch_start = time.time()
            train_metrics = train_one_epoch(model, train_loader, optimizer, scheduler, device, class_weights)
            valid_metrics = evaluate_model(model, valid_loader, device)
            elapsed_epoch = (time.time() - epoch_start) / 60

            current_score = (valid_metrics["macro_f1"], valid_metrics["accuracy"])
            if current_score > best_valid_score:
                best_valid_score = current_score
                best_epoch = epoch
                best_state_dict = copy.deepcopy(model.state_dict())
                note = " <- saved best checkpoint"
            else:
                note = ""

            history_rows.append(
                {
                    "model_key": args.model_key,
                    "seed": seed,
                    "epoch": epoch,
                    "train_loss": train_metrics["loss"],
                    "train_accuracy": train_metrics["accuracy"],
                    "train_macro_f1": train_metrics["macro_f1"],
                    "valid_loss": valid_metrics["loss"],
                    "valid_accuracy": valid_metrics["accuracy"],
                    "valid_macro_f1": valid_metrics["macro_f1"],
                    "elapsed_minutes": elapsed_epoch,
                }
            )

            print(
                f"Epoch {epoch}/{args.epochs}{note} | "
                f"train loss={train_metrics['loss']:.4f}, acc={train_metrics['accuracy']:.4f}, macro_f1={train_metrics['macro_f1']:.4f} | "
                f"valid loss={valid_metrics['loss']:.4f}, acc={valid_metrics['accuracy']:.4f}, macro_f1={valid_metrics['macro_f1']:.4f} | "
                f"elapsed={elapsed_epoch:.2f} min",
                flush=True,
            )

        if best_state_dict is None:
            raise RuntimeError(f"No best checkpoint for seed {seed}")
        model.load_state_dict(best_state_dict)
        print(f"Loaded best_state_dict into model from epoch {best_epoch} before all test/target evaluation.", flush=True)

        target_loaders = [
            (
                target_name,
                make_dataloader(target_df, text_col, tokenizer, args.max_length, args.eval_batch_size, shuffle=False),
            )
            for target_name, target_df, text_col in targets
        ]

        elapsed_seed = (time.time() - seed_start) / 60
        for target_name, loader in target_loaders:
            metrics = evaluate_model(model, loader, device)
            row = metric_row(seed, target_name, best_epoch, metrics, elapsed_seed)
            all_rows.append(row)
            print(
                f"Target {target_name}: acc={row['accuracy']:.4f}, macro_f1={row['macro_f1']:.4f}, "
                f"REAL recall={row['real_recall']:.4f}, FAKE recall={row['fake_recall']:.4f}",
                flush=True,
            )

        del model
        if torch.cuda.is_available():
            torch.cuda.empty_cache()

    results_df = pd.DataFrame(all_rows)
    history_df = pd.DataFrame(history_rows)
    save_report(args.model_key, model_title, model_name, seeds, results_df, history_df, out_dir, figures_dir, use_class_weights=preset.get("use_class_weights", True))
    print("\nSaved cross-dataset transformer results to:", out_dir, flush=True)


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--model-key", required=True, choices=sorted(MODEL_PRESETS))
    parser.add_argument("--model-name", default=None)
    parser.add_argument("--model-title", default=None)
    parser.add_argument("--seeds", default="42,52,62,72,82")
    parser.add_argument("--epochs", type=int, default=3)
    parser.add_argument("--max-length", type=int, default=128)
    parser.add_argument("--train-batch-size", type=int, default=16)
    parser.add_argument("--eval-batch-size", type=int, default=64)
    parser.add_argument("--learning-rate", type=float, default=2e-5)
    parser.add_argument("--weight-decay", type=float, default=0.01)
    parser.add_argument("--warmup-ratio", type=float, default=0.1)
    parser.add_argument("--require-cuda", action="store_true")
    return parser.parse_args()


if __name__ == "__main__":
    run(parse_args())
