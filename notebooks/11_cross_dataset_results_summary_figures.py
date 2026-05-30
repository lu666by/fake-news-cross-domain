from __future__ import annotations

from datetime import datetime
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

from liar_utils import dataframe_to_markdown


PROJECT_ROOT = Path(__file__).resolve().parent.parent
RESULTS_DIR = PROJECT_ROOT / "results" / "cross_dataset"
FIGURES_DIR = RESULTS_DIR / "figures"
FIGURES_DIR.mkdir(parents=True, exist_ok=True)


def load_tfidf() -> pd.DataFrame:
    df = pd.read_csv(RESULTS_DIR / "cross_dataset_tfidf_liar_to_fakenewsnet.csv")
    return pd.DataFrame(
        {
            "model": "TF-IDF + Logistic Regression",
            "target": df["target"],
            "runs": 1,
            "accuracy_mean": df["accuracy"].astype(float),
            "accuracy_std": 0.0,
            "macro_f1_mean": df["macro_f1"].astype(float),
            "macro_f1_std": 0.0,
            "real_recall_mean": df["real_recall"].astype(float),
            "real_recall_std": 0.0,
            "fake_recall_mean": df["fake_recall"].astype(float),
            "fake_recall_std": 0.0,
        }
    )


def load_transformer(model: str, path_name: str) -> pd.DataFrame:
    df = pd.read_csv(RESULTS_DIR / path_name)
    df.insert(0, "model", model)
    return df


def format_table(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    numeric_cols = [
        "accuracy_mean",
        "accuracy_std",
        "macro_f1_mean",
        "macro_f1_std",
        "real_recall_mean",
        "real_recall_std",
        "fake_recall_mean",
        "fake_recall_std",
    ]
    for col in numeric_cols:
        out[col] = out[col].map(lambda x: f"{x:.4f}")
    return out


def make_figures(combined: pd.DataFrame) -> None:
    sns.set_theme(style="whitegrid")

    # Figure 1: Macro-F1 by model and target.
    plt.figure(figsize=(12, 6))
    ax = sns.barplot(data=combined, x="target", y="macro_f1_mean", hue="model")
    ax.set_title("Cross-Dataset Macro-F1: LIAR to FakeNewsNet Minimal")
    ax.set_xlabel("")
    ax.set_ylabel("Macro-F1")
    ax.set_ylim(0, 0.75)
    ax.tick_params(axis="x", rotation=20)
    plt.tight_layout()
    plt.savefig(FIGURES_DIR / "cross_dataset_model_macro_f1_comparison.png", dpi=220)
    plt.close()

    # Figure 2: Accuracy by model and target.
    plt.figure(figsize=(12, 6))
    ax = sns.barplot(data=combined, x="target", y="accuracy_mean", hue="model")
    ax.set_title("Cross-Dataset Accuracy: LIAR to FakeNewsNet Minimal")
    ax.set_xlabel("")
    ax.set_ylabel("Accuracy")
    ax.set_ylim(0, 0.75)
    ax.tick_params(axis="x", rotation=20)
    plt.tight_layout()
    plt.savefig(FIGURES_DIR / "cross_dataset_model_accuracy_comparison.png", dpi=220)
    plt.close()

    # Figure 3: FakeNewsNet combined recall trade-off.
    target_df = combined[combined["target"] == "FakeNewsNet combined titles"].copy()
    recall_df = target_df.melt(
        id_vars=["model"],
        value_vars=["real_recall_mean", "fake_recall_mean"],
        var_name="metric",
        value_name="score",
    )
    recall_df["metric"] = recall_df["metric"].replace(
        {
            "real_recall_mean": "REAL recall",
            "fake_recall_mean": "FAKE recall",
        }
    )
    plt.figure(figsize=(9, 5.5))
    ax = sns.barplot(data=recall_df, x="model", y="score", hue="metric")
    ax.set_title("FakeNewsNet Combined Titles: REAL vs FAKE Recall")
    ax.set_xlabel("")
    ax.set_ylabel("Recall")
    ax.set_ylim(0, 1)
    ax.tick_params(axis="x", rotation=12)
    plt.tight_layout()
    plt.savefig(FIGURES_DIR / "cross_dataset_combined_recall_tradeoff.png", dpi=220)
    plt.close()


def main() -> None:
    tfidf = load_tfidf()
    roberta = load_transformer(
        "Weighted RoBERTa",
        "cross_dataset_weighted_roberta_liar_to_fakenewsnet_summary.csv",
    )
    bert = load_transformer(
        "Weighted BERT",
        "cross_dataset_weighted_bert_liar_to_fakenewsnet_summary.csv",
    )
    unweighted_bert = load_transformer(
        "Unweighted BERT",
        "cross_dataset_unweighted_bert_liar_to_fakenewsnet_summary.csv",
    )

    combined = pd.concat([tfidf, roberta, bert, unweighted_bert], ignore_index=True)
    model_order = ["TF-IDF + Logistic Regression", "Weighted RoBERTa", "Weighted BERT", "Unweighted BERT"]
    target_order = [
        "LIAR test",
        "FakeNewsNet PolitiFact titles",
        "FakeNewsNet GossipCop titles",
        "FakeNewsNet combined titles",
    ]
    combined["model"] = pd.Categorical(combined["model"], categories=model_order, ordered=True)
    combined["target"] = pd.Categorical(combined["target"], categories=target_order, ordered=True)
    combined = combined.sort_values(["target", "model"]).reset_index(drop=True)

    combined.to_csv(RESULTS_DIR / "cross_dataset_model_comparison.csv", index=False)
    formatted = format_table(combined)
    formatted.to_csv(RESULTS_DIR / "cross_dataset_model_comparison_formatted.csv", index=False)
    make_figures(combined)

    thesis_lines = [
        "# Cross-Dataset Model Comparison",
        "",
        f"- Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}",
        "- Source training setup: LIAR",
        "- Target setup: FakeNewsNet minimal titles",
        "- Transformer results are 5-seed mean/std.",
        "- TF-IDF is deterministic, so std is reported as 0.0000.",
        "",
        "## Combined Results",
        "",
        dataframe_to_markdown(formatted),
        "",
        "## Key Findings",
        "",
        "- All models drop substantially from LIAR in-domain testing to FakeNewsNet title transfer.",
        "- TF-IDF achieves the best Macro-F1 on FakeNewsNet combined titles among the four completed transfer baselines, but it is still weak at 0.4745 Macro-F1.",
        "- Weighted RoBERTa is best on LIAR, but transfers poorly to FakeNewsNet combined titles, with 0.2358 Macro-F1.",
        "- Weighted BERT transfers slightly better than weighted RoBERTa on FakeNewsNet combined titles, with 0.2682 Macro-F1, but still performs poorly overall.",
        "- Unweighted BERT also transfers poorly, with 0.2806 Macro-F1 on FakeNewsNet combined titles.",
        "- The weighted and unweighted transformer models strongly over-predict FAKE on FakeNewsNet titles, producing very high FAKE recall but extremely low REAL recall.",
        "",
        "## Thesis Interpretation",
        "",
        "The cross-dataset results support the main dissertation argument: in-domain LIAR performance does not guarantee cross-dataset reliability. The strongest in-domain model, weighted RoBERTa, is not the strongest transfer model on FakeNewsNet titles. The unweighted BERT control shows a similar target-domain failure pattern, so the transfer problem should not be attributed only to class-weighted loss. This suggests that the transformer models may learn LIAR-specific decision boundaries that do not transfer cleanly to a different dataset and text type.",
        "",
        "The results must be interpreted carefully because FakeNewsNet minimal uses titles rather than full article text. The experiment is therefore a short-text transfer test from LIAR statements to FakeNewsNet titles.",
        "",
        "## Figures",
        "",
        "- `figures/cross_dataset_model_macro_f1_comparison.png`",
        "- `figures/cross_dataset_model_accuracy_comparison.png`",
        "- `figures/cross_dataset_combined_recall_tradeoff.png`",
        "",
    ]
    (RESULTS_DIR / "cross_dataset_model_comparison.md").write_text("\n".join(thesis_lines), encoding="utf-8")
    print("Saved comparison outputs to", RESULTS_DIR)


if __name__ == "__main__":
    main()
