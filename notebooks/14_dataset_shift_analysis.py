from __future__ import annotations

import math
import re
from collections import Counter
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS

from cross_dataset_utils import load_fakenewsnet_minimal
from liar_utils import ID2LABEL, load_binary_dataset_splits, make_liar_config


PROJECT_ROOT = Path(__file__).resolve().parent.parent
OUTPUT_DIR = PROJECT_ROOT / "results" / "dataset_shift_analysis"
FIGURES_DIR = OUTPUT_DIR / "figures"

TOKEN_RE = re.compile(r"[a-z][a-z']{2,}")
STOPWORDS = set(ENGLISH_STOP_WORDS) | {
    "said",
    "says",
    "say",
    "new",
    "news",
    "video",
    "photo",
    "photos",
}


def tokenize(text: str) -> list[str]:
    tokens = TOKEN_RE.findall(str(text).lower())
    return [token.strip("'") for token in tokens if token not in STOPWORDS]


def percentile(series: pd.Series, q: float) -> float:
    return float(series.quantile(q))


def dataframe_to_markdown(df: pd.DataFrame) -> str:
    return df.to_markdown(index=False)


def build_analysis_frame() -> pd.DataFrame:
    liar_config = make_liar_config(PROJECT_ROOT / "data" / "liar_dataset")
    liar_splits = load_binary_dataset_splits(liar_config)
    liar_frames = []
    for split, df in zip(["train", "valid", "test"], liar_splits):
        out = df[["id", "statement", "context", "y"]].copy()
        out = out.rename(columns={"statement": "text"})
        out["dataset"] = "LIAR"
        out["split"] = split
        out["text_type"] = "statement"
        out["source"] = "liar"
        out["body_available"] = True
        liar_frames.append(out[["dataset", "split", "source", "id", "text_type", "text", "context", "body_available", "y"]])

    fnn = load_fakenewsnet_minimal(PROJECT_ROOT / "data" / "fakenewsnet_minimal" / "raw")
    fnn_out = fnn[["id", "source", "text", "y"]].copy()
    fnn_out["dataset"] = "FakeNewsNet"
    fnn_out["split"] = "all"
    fnn_out["text_type"] = "title"
    fnn_out["context"] = ""
    fnn_out["body_available"] = False

    rows = pd.concat([*liar_frames, fnn_out[["dataset", "split", "source", "id", "text_type", "text", "context", "body_available", "y"]]], ignore_index=True)
    rows["label"] = rows["y"].map(ID2LABEL)
    rows["char_len"] = rows["text"].fillna("").astype(str).str.len()
    rows["word_len"] = rows["text"].fillna("").astype(str).str.split().str.len()
    rows["context_char_len"] = rows["context"].fillna("").astype(str).str.len()
    rows["tokens"] = rows["text"].map(tokenize)
    rows["token_count"] = rows["tokens"].map(len)
    return rows


def length_summary(rows: pd.DataFrame) -> pd.DataFrame:
    grouped = rows.groupby(["dataset", "text_type", "label"], sort=False)
    out = grouped.agg(
        rows=("text", "size"),
        char_mean=("char_len", "mean"),
        char_median=("char_len", "median"),
        char_p90=("char_len", lambda s: percentile(s, 0.90)),
        word_mean=("word_len", "mean"),
        word_median=("word_len", "median"),
        word_p90=("word_len", lambda s: percentile(s, 0.90)),
        body_available=("body_available", "first"),
    ).reset_index()
    for col in ["char_mean", "char_median", "char_p90", "word_mean", "word_median", "word_p90"]:
        out[col] = out[col].round(2)
    return out


def top_terms(rows: pd.DataFrame, n: int = 20) -> pd.DataFrame:
    records = []
    for (dataset, label), group in rows.groupby(["dataset", "label"], sort=False):
        counter: Counter[str] = Counter()
        for toks in group["tokens"]:
            counter.update(toks)
        total = sum(counter.values())
        for rank, (term, count) in enumerate(counter.most_common(n), start=1):
            records.append(
                {
                    "dataset": dataset,
                    "label": label,
                    "rank": rank,
                    "term": term,
                    "count": count,
                    "per_1k_tokens": round(1000 * count / total, 2) if total else 0.0,
                }
            )
    return pd.DataFrame(records)


def vocabulary_overlap(rows: pd.DataFrame) -> pd.DataFrame:
    liar_vocab = set(token for toks in rows.loc[rows["dataset"] == "LIAR", "tokens"] for token in toks)
    fnn_vocab = set(token for toks in rows.loc[rows["dataset"] == "FakeNewsNet", "tokens"] for token in toks)

    liar_counter: Counter[str] = Counter()
    fnn_counter: Counter[str] = Counter()
    for toks in rows.loc[rows["dataset"] == "LIAR", "tokens"]:
        liar_counter.update(toks)
    for toks in rows.loc[rows["dataset"] == "FakeNewsNet", "tokens"]:
        fnn_counter.update(toks)

    records = []
    for n in [100, 250, 500, 1000, 2000]:
        liar_top = {term for term, _ in liar_counter.most_common(n)}
        fnn_top = {term for term, _ in fnn_counter.most_common(n)}
        overlap = liar_top & fnn_top
        union = liar_top | fnn_top
        records.append(
            {
                "vocab_scope": f"top_{n}",
                "liar_vocab": len(liar_top),
                "fakenewsnet_vocab": len(fnn_top),
                "overlap": len(overlap),
                "jaccard": round(len(overlap) / len(union), 4) if union else 0.0,
                "fnn_terms_seen_in_liar_pct": round(100 * len(overlap) / len(fnn_top), 2) if fnn_top else 0.0,
                "liar_terms_seen_in_fnn_pct": round(100 * len(overlap) / len(liar_top), 2) if liar_top else 0.0,
            }
        )

    overlap_all = liar_vocab & fnn_vocab
    union_all = liar_vocab | fnn_vocab
    records.append(
        {
            "vocab_scope": "all_terms",
            "liar_vocab": len(liar_vocab),
            "fakenewsnet_vocab": len(fnn_vocab),
            "overlap": len(overlap_all),
            "jaccard": round(len(overlap_all) / len(union_all), 4) if union_all else 0.0,
            "fnn_terms_seen_in_liar_pct": round(100 * len(overlap_all) / len(fnn_vocab), 2) if fnn_vocab else 0.0,
            "liar_terms_seen_in_fnn_pct": round(100 * len(overlap_all) / len(liar_vocab), 2) if liar_vocab else 0.0,
        }
    )
    return pd.DataFrame(records)


def log_odds_terms(rows: pd.DataFrame, group_col: str, value_a: str, value_b: str, top_n: int = 20) -> pd.DataFrame:
    counter_a: Counter[str] = Counter()
    counter_b: Counter[str] = Counter()
    for toks in rows.loc[rows[group_col] == value_a, "tokens"]:
        counter_a.update(toks)
    for toks in rows.loc[rows[group_col] == value_b, "tokens"]:
        counter_b.update(toks)

    vocab = sorted(set(counter_a) | set(counter_b))
    total_a = sum(counter_a.values())
    total_b = sum(counter_b.values())
    vocab_size = len(vocab)
    records = []
    for term in vocab:
        a = counter_a[term] + 1
        b = counter_b[term] + 1
        odds_a = a / (total_a + vocab_size - a)
        odds_b = b / (total_b + vocab_size - b)
        score = math.log(odds_a / odds_b)
        records.append(
            {
                "comparison": f"{value_a} vs {value_b}",
                "term": term,
                f"{value_a}_count": counter_a[term],
                f"{value_b}_count": counter_b[term],
                "log_odds_toward_first": score,
            }
        )
    scored = pd.DataFrame(records)
    top_a = scored.sort_values("log_odds_toward_first", ascending=False).head(top_n).copy()
    top_a["direction"] = value_a
    top_b = scored.sort_values("log_odds_toward_first", ascending=True).head(top_n).copy()
    top_b["direction"] = value_b
    top_b["log_odds_toward_first"] = top_b["log_odds_toward_first"].abs()
    out = pd.concat([top_a, top_b], ignore_index=True)
    out["log_odds_abs"] = out["log_odds_toward_first"].round(3)
    return out.drop(columns=["log_odds_toward_first"])


def label_distinctive_terms(rows: pd.DataFrame, top_n: int = 15) -> pd.DataFrame:
    outputs = []
    for dataset, group in rows.groupby("dataset", sort=False):
        scored = log_odds_terms(group, "label", "FAKE", "REAL", top_n=top_n)
        scored.insert(0, "dataset", dataset)
        outputs.append(scored)
    return pd.concat(outputs, ignore_index=True)


def plot_lengths(rows: pd.DataFrame) -> None:
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)
    plt.figure(figsize=(9, 5))
    sns.boxplot(data=rows, x="dataset", y="word_len", hue="label", showfliers=False)
    plt.ylabel("Word length")
    plt.xlabel("")
    plt.title("Main Text Length by Dataset and Label")
    plt.tight_layout()
    plt.savefig(FIGURES_DIR / "word_length_by_dataset_label.png", dpi=200)
    plt.close()


def plot_top_terms(top_df: pd.DataFrame) -> None:
    plot_df = top_df[(top_df["rank"] <= 10) & (top_df["label"] == "FAKE")].copy()
    g = sns.catplot(
        data=plot_df,
        x="per_1k_tokens",
        y="term",
        col="dataset",
        kind="bar",
        height=5,
        aspect=0.9,
        sharey=False,
        color="#4C78A8",
    )
    g.set_axis_labels("Occurrences per 1k tokens", "")
    g.set_titles("{col_name} FAKE top terms")
    plt.tight_layout()
    plt.savefig(FIGURES_DIR / "fake_top_terms_by_dataset.png", dpi=200)
    plt.close()


def plot_vocab_overlap(overlap: pd.DataFrame) -> None:
    plot_df = overlap[overlap["vocab_scope"].str.startswith("top_")].copy()
    plot_df["top_n"] = plot_df["vocab_scope"].str.replace("top_", "", regex=False).astype(int)
    plt.figure(figsize=(8, 4.5))
    sns.lineplot(data=plot_df, x="top_n", y="jaccard", marker="o")
    plt.xlabel("Top-N vocabulary scope")
    plt.ylabel("Jaccard overlap")
    plt.title("Vocabulary Overlap between LIAR and FakeNewsNet")
    plt.tight_layout()
    plt.savefig(FIGURES_DIR / "vocabulary_overlap_topn.png", dpi=200)
    plt.close()


def plot_dataset_distinctive(distinctive: pd.DataFrame) -> None:
    plot_df = distinctive.head(12).copy()
    plot_df = pd.concat([distinctive[distinctive["direction"] == "LIAR"].head(8), distinctive[distinctive["direction"] == "FakeNewsNet"].head(8)])
    plt.figure(figsize=(9, 5.5))
    sns.barplot(data=plot_df, x="log_odds_abs", y="term", hue="direction")
    plt.xlabel("Absolute log-odds score")
    plt.ylabel("")
    plt.title("Dataset-Distinctive Terms")
    plt.tight_layout()
    plt.savefig(FIGURES_DIR / "dataset_distinctive_terms.png", dpi=200)
    plt.close()


def write_report(
    length_df: pd.DataFrame,
    overlap_df: pd.DataFrame,
    dataset_distinctive: pd.DataFrame,
    label_distinctive: pd.DataFrame,
) -> None:
    report = [
        "# LIAR vs FakeNewsNet Dataset-Shift Analysis",
        "",
        "- Date: 2026-05-30",
        "- Purpose: explain why LIAR -> FakeNewsNet transfer is difficult and why title-only evaluation can behave differently from longer/full-text settings.",
        "- Important data limitation: FakeNewsNet Minimal contains titles only; article body text is unavailable in the local dataset. Therefore, the main comparison is LIAR `statement` text vs FakeNewsNet `title` text.",
        "",
        "## Length Summary",
        "",
        dataframe_to_markdown(length_df),
        "",
        "## Vocabulary Overlap",
        "",
        dataframe_to_markdown(overlap_df),
        "",
        "## Dataset-Distinctive Terms",
        "",
        dataframe_to_markdown(dataset_distinctive.head(30)),
        "",
        "## Label-Distinctive Terms",
        "",
        dataframe_to_markdown(label_distinctive.head(40)),
        "",
        "## Thesis-Ready Interpretation",
        "",
        "LIAR and FakeNewsNet Minimal differ not only in label source but also in text form. LIAR examples are short fact-checking statements, while the available FakeNewsNet Minimal target data consists of news titles. This means that the transfer experiment is a statement-to-title transfer setting rather than full-article fake-news detection.",
        "",
        "The length analysis shows that both datasets are short-text settings, but their distributions and lexical signals are not identical. FakeNewsNet titles contain outlet/topic/headline vocabulary, whereas LIAR statements contain political-claim vocabulary and fact-checking-style phrasing. This helps explain why a model trained on LIAR can preserve a strong FAKE bias when moved to FakeNewsNet: it learns source-domain lexical and stylistic cues that do not map cleanly onto the target title domain.",
        "",
        "The vocabulary-overlap table shows limited overlap even among high-frequency terms. This supports the interpretation that cross-dataset failure is driven by domain and style shift, not simply by model weakness. Title-only evaluation may sometimes look slightly different from longer-text settings because titles are short, selective, and headline-like; they may remove some article-body noise, but they also amplify style and topic mismatch.",
        "",
        "These analyses should be used as explanatory evidence, not as predictive features. Their role is to justify the dissertation's interpretation: strict LIAR -> FakeNewsNet transfer is hard because the target data changes both the domain and the text genre, and intermediate target-domain fine-tuning helps because it exposes the model to target-title vocabulary and label associations.",
        "",
        "## Generated Figures",
        "",
        "- `figures/word_length_by_dataset_label.png`",
        "- `figures/fake_top_terms_by_dataset.png`",
        "- `figures/vocabulary_overlap_topn.png`",
        "- `figures/dataset_distinctive_terms.png`",
        "",
    ]
    (OUTPUT_DIR / "liar_vs_fakenewsnet_explanation_20260530.md").write_text("\n".join(report), encoding="utf-8")


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)

    rows = build_analysis_frame()
    rows.drop(columns=["tokens"]).to_csv(OUTPUT_DIR / "analysis_rows.csv", index=False)

    length_df = length_summary(rows)
    terms_df = top_terms(rows, n=25)
    overlap_df = vocabulary_overlap(rows)
    dataset_distinctive = log_odds_terms(rows, "dataset", "LIAR", "FakeNewsNet", top_n=25)
    label_distinctive = label_distinctive_terms(rows, top_n=15)

    length_df.to_csv(OUTPUT_DIR / "length_summary_by_dataset_label.csv", index=False)
    terms_df.to_csv(OUTPUT_DIR / "top_terms_by_dataset_label.csv", index=False)
    overlap_df.to_csv(OUTPUT_DIR / "vocabulary_overlap.csv", index=False)
    dataset_distinctive.to_csv(OUTPUT_DIR / "dataset_distinctive_terms.csv", index=False)
    label_distinctive.to_csv(OUTPUT_DIR / "label_distinctive_terms.csv", index=False)

    (OUTPUT_DIR / "length_summary_by_dataset_label.md").write_text(dataframe_to_markdown(length_df), encoding="utf-8")
    (OUTPUT_DIR / "top_terms_by_dataset_label.md").write_text(dataframe_to_markdown(terms_df), encoding="utf-8")
    (OUTPUT_DIR / "vocabulary_overlap.md").write_text(dataframe_to_markdown(overlap_df), encoding="utf-8")
    (OUTPUT_DIR / "dataset_distinctive_terms.md").write_text(dataframe_to_markdown(dataset_distinctive), encoding="utf-8")
    (OUTPUT_DIR / "label_distinctive_terms.md").write_text(dataframe_to_markdown(label_distinctive), encoding="utf-8")

    sns.set_theme(style="whitegrid")
    plot_lengths(rows)
    plot_top_terms(terms_df)
    plot_vocab_overlap(overlap_df)
    plot_dataset_distinctive(dataset_distinctive)

    write_report(length_df, overlap_df, dataset_distinctive, label_distinctive)
    print(f"Saved dataset-shift analysis to {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
