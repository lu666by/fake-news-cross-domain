from __future__ import annotations

from pathlib import Path
from typing import Iterable

import pandas as pd
from sklearn.metrics import recall_score

from liar_utils import clean_text_series, evaluate_predictions


FAKENEWSNET_FILES = {
    ("politifact", 1): "politifact_fake.csv",
    ("politifact", 0): "politifact_real.csv",
    ("gossipcop", 1): "gossipcop_fake.csv",
    ("gossipcop", 0): "gossipcop_real.csv",
}


def find_project_root() -> Path:
    current = Path.cwd().resolve()
    for path in [current, *current.parents]:
        if (path / "data").exists() and (path / "notebooks").exists():
            return path
    raise FileNotFoundError("Could not find project root with data/ and notebooks/.")


def load_fakenewsnet_minimal(raw_dir: str | Path) -> pd.DataFrame:
    raw_dir = Path(raw_dir)
    frames = []

    for (source, label), filename in FAKENEWSNET_FILES.items():
        path = raw_dir / filename
        if not path.exists():
            raise FileNotFoundError(f"Missing FakeNewsNet minimal file: {path}")
        df = pd.read_csv(path)
        df = df.copy()
        df["source"] = source
        df["y"] = label
        df["label_name"] = df["y"].map({0: "REAL", 1: "FAKE"})
        df["text"] = clean_text_series(df["title"])
        frames.append(df[["id", "source", "y", "label_name", "text", "news_url", "tweet_ids"]])

    out = pd.concat(frames, ignore_index=True)
    out = out[out["text"] != ""].copy()
    return out


def add_text_length_columns(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    out["char_len"] = out["text"].str.len()
    out["word_len"] = out["text"].str.split().str.len()
    return out


def make_eval_row(name: str, y_true: Iterable[int], y_pred: Iterable[int]) -> dict:
    metrics = evaluate_predictions(y_true, y_pred)
    real_recall, fake_recall = recall_score(
        y_true,
        y_pred,
        labels=[0, 1],
        average=None,
        zero_division=0,
    )
    return {
        "target": name,
        "n": len(list(y_true)) if not hasattr(y_true, "__len__") else len(y_true),
        "accuracy": metrics["accuracy"],
        "macro_f1": metrics["macro_f1"],
        "real_recall": real_recall,
        "fake_recall": fake_recall,
        "confusion_matrix": metrics["confusion_matrix"].tolist(),
        "classification_report": metrics["classification_report"],
    }


def format_float(value: float) -> str:
    return f"{value:.4f}"
