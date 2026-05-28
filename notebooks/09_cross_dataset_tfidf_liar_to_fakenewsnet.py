from __future__ import annotations

from datetime import datetime
from pathlib import Path

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

from cross_dataset_utils import (
    add_text_length_columns,
    find_project_root,
    format_float,
    load_fakenewsnet_minimal,
    make_eval_row,
)
from liar_utils import (
    dataframe_to_markdown,
    load_binary_dataset_splits,
    make_liar_config,
)


PROJECT_ROOT = find_project_root()
LIAR_DIR = PROJECT_ROOT / "data" / "liar_dataset"
FNN_RAW_DIR = PROJECT_ROOT / "data" / "fakenewsnet_minimal" / "raw"
FNN_PROCESSED_DIR = PROJECT_ROOT / "data" / "fakenewsnet_minimal" / "processed"
INSPECTION_DIR = PROJECT_ROOT / "results" / "data_inspection"
CROSS_RESULTS_DIR = PROJECT_ROOT / "results" / "cross_dataset"

for directory in [FNN_PROCESSED_DIR, INSPECTION_DIR, CROSS_RESULTS_DIR]:
    directory.mkdir(parents=True, exist_ok=True)


def save_fakenewsnet_inspection(fnn: pd.DataFrame) -> None:
    inspected = add_text_length_columns(fnn)
    processed_path = FNN_PROCESSED_DIR / "fakenewsnet_minimal_titles.csv"
    inspected.to_csv(processed_path, index=False)

    source_label_counts = (
        inspected.groupby(["source", "label_name"])
        .size()
        .reset_index(name="count")
        .sort_values(["source", "label_name"])
    )
    length_stats = (
        inspected.groupby(["source", "label_name"])[["char_len", "word_len"]]
        .agg(["count", "mean", "median", "min", "max"])
        .round(2)
    )
    length_stats.columns = ["_".join(col).strip() for col in length_stats.columns.values]
    length_stats = length_stats.reset_index()

    missing_titles = int((inspected["text"] == "").sum())
    duplicate_titles = int(inspected["text"].duplicated().sum())

    source_label_counts.to_csv(INSPECTION_DIR / "fakenewsnet_minimal_label_counts.csv", index=False)
    length_stats.to_csv(INSPECTION_DIR / "fakenewsnet_minimal_title_length_stats.csv", index=False)

    report = [
        "# FakeNewsNet Minimal Inspection",
        "",
        f"- Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}",
        f"- Raw directory: `{FNN_RAW_DIR.relative_to(PROJECT_ROOT)}`",
        f"- Processed CSV: `{processed_path.relative_to(PROJECT_ROOT)}`",
        "- Text field used for modelling: `title` -> unified as `text`",
        "- Label mapping: REAL=0, FAKE=1",
        "",
        "## Basic Counts",
        "",
        f"- Total usable rows: `{len(inspected)}`",
        f"- Empty titles after cleaning: `{missing_titles}`",
        f"- Duplicate cleaned titles: `{duplicate_titles}`",
        "",
        "## Counts by Source and Label",
        "",
        dataframe_to_markdown(source_label_counts),
        "",
        "## Title Length Statistics",
        "",
        dataframe_to_markdown(length_stats),
        "",
        "## Important Limitation",
        "",
        "FakeNewsNet minimal contains `title`, not full article text. Therefore the cross-dataset experiment should be described as LIAR `statement` to FakeNewsNet `title` transfer.",
        "",
    ]
    (INSPECTION_DIR / "fakenewsnet_minimal_inspection.md").write_text(
        "\n".join(report),
        encoding="utf-8",
    )


def train_liar_tfidf():
    config = make_liar_config(LIAR_DIR)
    train_df, valid_df, test_df = load_binary_dataset_splits(config)
    train_valid_df = pd.concat([train_df, valid_df], axis=0, ignore_index=True)

    vectorizer = TfidfVectorizer(
        ngram_range=(1, 2),
        min_df=2,
        max_df=1.0,
        lowercase=True,
    )
    model = LogisticRegression(
        max_iter=2000,
        C=1.0,
        solver="lbfgs",
        random_state=42,
    )

    x_train = vectorizer.fit_transform(train_valid_df[config.text_column])
    model.fit(x_train, train_valid_df["y"])

    return config, vectorizer, model, train_df, valid_df, train_valid_df, test_df


def evaluate_targets(config, vectorizer, model, test_df, fnn: pd.DataFrame) -> list[dict]:
    targets = [
        ("LIAR test", test_df[config.text_column], test_df["y"]),
        (
            "FakeNewsNet PolitiFact titles",
            fnn.loc[fnn["source"] == "politifact", "text"],
            fnn.loc[fnn["source"] == "politifact", "y"],
        ),
        (
            "FakeNewsNet GossipCop titles",
            fnn.loc[fnn["source"] == "gossipcop", "text"],
            fnn.loc[fnn["source"] == "gossipcop", "y"],
        ),
        ("FakeNewsNet combined titles", fnn["text"], fnn["y"]),
    ]

    rows = []
    for name, texts, labels in targets:
        preds = model.predict(vectorizer.transform(texts))
        rows.append(make_eval_row(name, labels.to_numpy(), preds))
    return rows


def save_cross_dataset_results(rows: list[dict]) -> None:
    full_df = pd.DataFrame(rows)
    compact_cols = [
        "target",
        "n",
        "accuracy",
        "macro_f1",
        "real_recall",
        "fake_recall",
        "confusion_matrix",
    ]
    compact_df = full_df[compact_cols].copy()
    for col in ["accuracy", "macro_f1", "real_recall", "fake_recall"]:
        compact_df[col] = compact_df[col].map(format_float)

    full_df.to_csv(CROSS_RESULTS_DIR / "cross_dataset_tfidf_liar_to_fakenewsnet_full.csv", index=False)
    compact_df.to_csv(CROSS_RESULTS_DIR / "cross_dataset_tfidf_liar_to_fakenewsnet.csv", index=False)

    report_lines = [
        "# Cross-Dataset TF-IDF: LIAR to FakeNewsNet Minimal",
        "",
        f"- Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}",
        "- Final training data: LIAR train + validation splits after selecting the existing TF-IDF V2 configuration",
        "- Source test: LIAR test split",
        "- Target dataset: FakeNewsNet minimal titles",
        "- Input transfer setting: LIAR `statement` -> FakeNewsNet `title`",
        "- Model: TF-IDF `(1,2)` + Logistic Regression",
        "- TF-IDF fit only on LIAR train + validation text",
        "- No FakeNewsNet rows used for training or tuning",
        "",
        "## Compact Results",
        "",
        dataframe_to_markdown(compact_df),
        "",
        "## Interpretation",
        "",
        "- This is the first strict cross-dataset baseline in the project.",
        "- The model is trained only on LIAR and directly evaluated on FakeNewsNet titles.",
        "- The FakeNewsNet minimal target is title-only, so results should not be described as full-article fake news detection.",
        "- A large performance drop from LIAR to FakeNewsNet would support the dissertation argument that in-domain performance does not guarantee cross-dataset reliability.",
        "",
    ]

    for row in rows:
        report_lines.extend(
            [
                f"## Classification Report: {row['target']}",
                "",
                "```text",
                row["classification_report"].strip(),
                "```",
                "",
            ]
        )

    (CROSS_RESULTS_DIR / "cross_dataset_tfidf_liar_to_fakenewsnet.md").write_text(
        "\n".join(report_lines),
        encoding="utf-8",
    )


def main() -> None:
    print("Loading FakeNewsNet minimal...")
    fnn = load_fakenewsnet_minimal(FNN_RAW_DIR)
    save_fakenewsnet_inspection(fnn)
    print(f"FakeNewsNet usable rows: {len(fnn)}")

    print("Training LIAR TF-IDF baseline...")
    config, vectorizer, model, train_df, valid_df, train_valid_df, test_df = train_liar_tfidf()
    print(f"LIAR train rows: {len(train_df)}")
    print(f"LIAR train+valid rows used for final TF-IDF fit: {len(train_valid_df)}")

    print("Evaluating LIAR and FakeNewsNet targets...")
    rows = evaluate_targets(config, vectorizer, model, test_df, fnn)
    save_cross_dataset_results(rows)

    print("\nCompact results:")
    compact = pd.DataFrame(rows)[
        ["target", "n", "accuracy", "macro_f1", "real_recall", "fake_recall", "confusion_matrix"]
    ]
    print(compact.to_string(index=False))
    print("\nSaved:")
    print(" ", INSPECTION_DIR / "fakenewsnet_minimal_inspection.md")
    print(" ", CROSS_RESULTS_DIR / "cross_dataset_tfidf_liar_to_fakenewsnet.md")


if __name__ == "__main__":
    main()
