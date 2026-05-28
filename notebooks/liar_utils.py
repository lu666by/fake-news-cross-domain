from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Mapping, Sequence

import pandas as pd
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix, f1_score


LIAR_COLUMNS = [
    "id",
    "label",
    "statement",
    "subject",
    "speaker",
    "speaker_job",
    "state",
    "party",
    "barely_true_counts",
    "false_counts",
    "half_true_counts",
    "mostly_true_counts",
    "pants_on_fire_counts",
    "context",
]

BIN_MAP = {
    "true": 0,
    "mostly-true": 0,
    "half-true": 0,
    "barely-true": 1,
    "false": 1,
    "pants-fire": 1,
}

ID2LABEL = {
    0: "REAL",
    1: "FAKE",
}


@dataclass(frozen=True)
class BinaryTextDatasetConfig:
    name: str
    data_dir: Path
    columns: Sequence[str]
    split_files: Mapping[str, str]
    text_column: str = "statement"
    label_column: str = "label"
    sep: str = "\t"
    binary_map: Mapping[str, int] = field(default_factory=lambda: BIN_MAP.copy())

    def get_split_path(self, split: str) -> Path:
        if split not in self.split_files:
            raise KeyError(f"Unknown split: {split}")
        return self.data_dir / self.split_files[split]


def make_liar_config(data_dir: str | Path = Path(__file__).resolve().parent.parent / "data" / "liar_dataset") -> BinaryTextDatasetConfig:
    return BinaryTextDatasetConfig(
        name="LIAR",
        data_dir=Path(data_dir),
        columns=LIAR_COLUMNS,
        split_files={
            "train": "train.tsv",
            "valid": "valid.tsv",
            "test": "test.tsv",
        },
        text_column="statement",
        label_column="label",
        sep="\t",
        binary_map=BIN_MAP.copy(),
    )


def load_delimited_split(path: Path, columns: Sequence[str], sep: str = "\t") -> pd.DataFrame:
    if not path.exists():
        raise FileNotFoundError(
            f"File not found: {path}\n"
            "Please place the dataset files in the configured data directory."
        )
    return pd.read_csv(path, sep=sep, header=None, names=list(columns))


def clean_text_series(series: pd.Series) -> pd.Series:
    return (
        series.fillna("")
        .astype(str)
        .str.replace(r"\s+", " ", regex=True)
        .str.strip()
    )


def prepare_binary_split(
    df: pd.DataFrame,
    text_column: str,
    label_column: str,
    binary_map: Mapping[str, int],
) -> pd.DataFrame:
    out = df.copy()
    out[text_column] = clean_text_series(out[text_column])
    out = out[out[text_column] != ""].copy()
    out["y"] = out[label_column].map(binary_map)
    out = out.dropna(subset=["y"]).copy()
    out["y"] = out["y"].astype(int)
    return out


def load_binary_dataset_splits(
    config: BinaryTextDatasetConfig,
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    prepared_splits = []

    for split in ("train", "valid", "test"):
        raw_df = load_delimited_split(
            path=config.get_split_path(split),
            columns=config.columns,
            sep=config.sep,
        )
        prepared_df = prepare_binary_split(
            df=raw_df,
            text_column=config.text_column,
            label_column=config.label_column,
            binary_map=config.binary_map,
        )
        prepared_splits.append(prepared_df)

    return tuple(prepared_splits)


def show_binary_distribution(
    df: pd.DataFrame,
    name: str,
    id_to_label: Mapping[int, str] | None = None,
) -> None:
    label_names = id_to_label or ID2LABEL
    counts = df["y"].value_counts().sort_index()
    total = len(df)

    print(f"\n{name} binary distribution:")
    for class_id in sorted(label_names):
        count = int(counts.get(class_id, 0))
        pct = 100 * count / total if total else 0.0
        print(f"  {label_names[class_id]} ({class_id}): {count} ({pct:.2f}%)")


def evaluate_predictions(
    y_true,
    y_pred,
    *,
    label_order: Sequence[int] = (0, 1),
    target_names: Sequence[str] = ("REAL", "FAKE"),
    digits: int = 4,
) -> dict:
    accuracy = accuracy_score(y_true, y_pred)
    macro_f1 = f1_score(y_true, y_pred, average="macro")
    cm = confusion_matrix(y_true, y_pred, labels=list(label_order))
    report = classification_report(
        y_true,
        y_pred,
        labels=list(label_order),
        target_names=list(target_names),
        digits=digits,
    )

    return {
        "accuracy": accuracy,
        "macro_f1": macro_f1,
        "confusion_matrix": cm,
        "classification_report": report,
    }


def dataframe_to_markdown(df: pd.DataFrame) -> str:
    columns = list(df.columns)
    lines = [
        "| " + " | ".join(columns) + " |",
        "| " + " | ".join(["---"] * len(columns)) + " |",
    ]

    for _, row in df.iterrows():
        values = [str(row[column]) for column in columns]
        lines.append("| " + " | ".join(values) + " |")

    return "\n".join(lines)
