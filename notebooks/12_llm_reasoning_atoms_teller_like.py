from __future__ import annotations

import argparse
import json
import os
import re
import time
import urllib.error
import urllib.request
from datetime import datetime
from pathlib import Path
from typing import Any

import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.model_selection import train_test_split

from cross_dataset_utils import find_project_root, format_float, load_fakenewsnet_minimal, make_eval_row
from liar_utils import dataframe_to_markdown, load_binary_dataset_splits, make_liar_config


PROJECT_ROOT = find_project_root()
LIAR_DIR = PROJECT_ROOT / "data" / "liar_dataset"
FNN_RAW_DIR = PROJECT_ROOT / "data" / "fakenewsnet_minimal" / "raw"
RESULTS_DIR = PROJECT_ROOT / "results" / "llm_reasoning_atoms"
FEATURE_CACHE = RESULTS_DIR / "llm_reasoning_atoms_features.jsonl"

ATOM_COLUMNS = [
    "emotional_language",
    "exaggerated_claim",
    "specific_evidence",
    "source_reference",
    "logical_consistency",
    "clickbait_style",
]

SYSTEM_PROMPT = """You are annotating short political/news texts for a fake-news detection research experiment.
Do not decide whether the text is fake or real.
Return only a compact JSON object with binary reasoning-signal fields."""

USER_PROMPT_TEMPLATE = """Text:
{text}

Return exactly this JSON schema:
{{
  "emotional_language": 0 or 1,
  "exaggerated_claim": 0 or 1,
  "specific_evidence": 0 or 1,
  "source_reference": 0 or 1,
  "logical_consistency": 0 or 1,
  "clickbait_style": 0 or 1,
  "reason": "one short sentence explaining the signal choices"
}}

Field meanings:
- emotional_language: 1 if the text uses obvious emotional or loaded wording.
- exaggerated_claim: 1 if the claim appears unusually broad, sensational, or extreme.
- specific_evidence: 1 if it contains concrete evidence, numbers, named documents, or verifiable details.
- source_reference: 1 if it explicitly names a source, institution, study, person, or outlet.
- logical_consistency: 1 if the statement is internally coherent; 0 if it has obvious internal tension or ambiguity.
- clickbait_style: 1 if it resembles headline bait, sensational framing, or curiosity-gap style.
"""


def stable_row_id(dataset: str, split: str, raw_id: Any, index: int) -> str:
    cleaned = re.sub(r"[^A-Za-z0-9_.-]+", "_", str(raw_id)).strip("_")
    if not cleaned:
        cleaned = str(index)
    return f"{dataset}:{split}:{cleaned}"


def load_experiment_rows(fnn_test_size: float = 0.2, seed: int = 42) -> pd.DataFrame:
    config = make_liar_config(LIAR_DIR)
    liar_train, liar_valid, liar_test = load_binary_dataset_splits(config)
    liar_frames = []
    for split, df in [("train", liar_train), ("valid", liar_valid), ("test", liar_test)]:
        out = df[["id", config.text_column, "y"]].copy()
        out = out.rename(columns={config.text_column: "text"})
        out["dataset"] = "liar"
        out["split"] = split
        liar_frames.append(out)

    fnn = load_fakenewsnet_minimal(FNN_RAW_DIR)
    fnn_train, fnn_test = train_test_split(
        fnn,
        test_size=fnn_test_size,
        random_state=seed,
        stratify=fnn["y"],
    )
    fnn_frames = []
    for split, df in [("train", fnn_train), ("test", fnn_test)]:
        out = df[["id", "text", "y", "source"]].copy()
        out["dataset"] = "fakenewsnet"
        out["split"] = split
        fnn_frames.append(out)

    rows = pd.concat([*liar_frames, *fnn_frames], ignore_index=True)
    rows["row_id"] = [
        stable_row_id(dataset, split, raw_id, index)
        for index, (dataset, split, raw_id) in enumerate(zip(rows["dataset"], rows["split"], rows["id"]))
    ]
    return rows[["row_id", "dataset", "split", "id", "text", "y"] + (["source"] if "source" in rows.columns else [])]


def load_feature_cache(path: Path = FEATURE_CACHE) -> dict[str, dict[str, Any]]:
    if not path.exists():
        return {}
    cache: dict[str, dict[str, Any]] = {}
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            if line.strip():
                item = json.loads(line)
                cache[item["row_id"]] = item
    return cache


def append_feature(item: dict[str, Any], path: Path = FEATURE_CACHE) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(item, ensure_ascii=False) + "\n")


def parse_json_object(text: str) -> dict[str, Any]:
    text = text.strip()
    match = re.search(r"\{.*\}", text, flags=re.DOTALL)
    if match:
        text = match.group(0)
    data = json.loads(text)
    cleaned: dict[str, Any] = {}
    for col in ATOM_COLUMNS:
        value = int(data.get(col, 0))
        cleaned[col] = 1 if value else 0
    cleaned["reason"] = str(data.get("reason", "")).strip()[:300]
    return cleaned


def http_json(url: str, payload: dict[str, Any], headers: dict[str, str] | None = None, timeout: int = 90) -> dict[str, Any]:
    request = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json", **(headers or {})},
        method="POST",
    )
    with urllib.request.urlopen(request, timeout=timeout) as response:
        return json.loads(response.read().decode("utf-8"))


def call_openai(text: str, model: str) -> dict[str, Any]:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is not set.")
    payload = {
        "model": model,
        "temperature": 0,
        "response_format": {"type": "json_object"},
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": USER_PROMPT_TEMPLATE.format(text=text[:2500])},
        ],
    }
    response = http_json(
        "https://api.openai.com/v1/chat/completions",
        payload,
        headers={"Authorization": f"Bearer {api_key}"},
    )
    content = response["choices"][0]["message"]["content"]
    return parse_json_object(content)


def call_deepseek(text: str, model: str) -> dict[str, Any]:
    api_key = os.environ.get("DEEPSEEK_API_KEY")
    if not api_key:
        raise RuntimeError("DEEPSEEK_API_KEY is not set.")
    payload = {
        "model": model,
        "temperature": 0,
        "response_format": {"type": "json_object"},
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": USER_PROMPT_TEMPLATE.format(text=text[:2500])},
        ],
    }
    response = http_json(
        "https://api.deepseek.com/chat/completions",
        payload,
        headers={"Authorization": f"Bearer {api_key}"},
    )
    content = response["choices"][0]["message"]["content"]
    return parse_json_object(content)


def call_ollama(text: str, model: str, base_url: str) -> dict[str, Any]:
    payload = {
        "model": model,
        "stream": False,
        "format": "json",
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": USER_PROMPT_TEMPLATE.format(text=text[:2500])},
        ],
        "options": {"temperature": 0},
    }
    response = http_json(f"{base_url.rstrip('/')}/api/chat", payload)
    return parse_json_object(response["message"]["content"])


def call_llm(text: str, provider: str, model: str, ollama_url: str) -> dict[str, Any]:
    if provider == "openai":
        return call_openai(text, model)
    if provider == "deepseek":
        return call_deepseek(text, model)
    if provider == "ollama":
        return call_ollama(text, model, ollama_url)
    raise ValueError(f"Unknown provider: {provider}")


def sample_rows(rows: pd.DataFrame, max_per_group: int | None, seed: int) -> pd.DataFrame:
    if not max_per_group:
        return rows
    groups = []
    for _, group in rows.groupby(["dataset", "split", "y"], sort=False):
        groups.append(group.sample(n=min(max_per_group, len(group)), random_state=seed))
    return pd.concat(groups, ignore_index=True)


def generate_missing_features(args: argparse.Namespace) -> None:
    rows = load_experiment_rows(seed=args.seed)
    rows = sample_rows(rows, args.max_per_group, args.seed)
    cache = load_feature_cache()
    missing = rows[~rows["row_id"].isin(cache.keys())].copy()

    print(f"Rows selected: {len(rows)}")
    print(f"Cached rows: {len(cache)}")
    print(f"Missing rows to annotate: {len(missing)}")
    if args.dry_run:
        example = missing.iloc[0] if len(missing) else rows.iloc[0]
        print("\nDry-run prompt example:\n")
        print(USER_PROMPT_TEMPLATE.format(text=example["text"]))
        return

    for index, row in enumerate(missing.itertuples(index=False), start=1):
        for attempt in range(1, args.retries + 1):
            try:
                atoms = call_llm(row.text, args.provider, args.model, args.ollama_url)
                item = {
                    "row_id": row.row_id,
                    "dataset": row.dataset,
                    "split": row.split,
                    "label": int(row.y),
                    "text": row.text,
                    "provider": args.provider,
                    "model": args.model,
                    "created_at": datetime.now().isoformat(timespec="seconds"),
                    **atoms,
                }
                append_feature(item)
                break
            except (json.JSONDecodeError, KeyError, RuntimeError, OSError, urllib.error.URLError) as exc:
                if attempt >= args.retries:
                    raise
                wait = args.sleep_seconds * attempt
                print(f"Retry {attempt}/{args.retries} after error: {exc}. Waiting {wait:.1f}s")
                time.sleep(wait)
        if index % 25 == 0 or index == len(missing):
            print(f"Annotated {index}/{len(missing)} missing rows")
        time.sleep(args.sleep_seconds)


def features_dataframe() -> pd.DataFrame:
    cache = load_feature_cache()
    if not cache:
        raise FileNotFoundError(f"No feature cache found at {FEATURE_CACHE}")
    df = pd.DataFrame(cache.values())
    for col in ATOM_COLUMNS:
        df[col] = df[col].astype(int)
    df["label"] = df["label"].astype(int)
    return df


def train_classifier(name: str, model_type: str):
    if model_type == "lr":
        return LogisticRegression(max_iter=1000, class_weight="balanced", random_state=42)
    if model_type == "rf":
        return RandomForestClassifier(n_estimators=300, class_weight="balanced", random_state=42)
    raise ValueError(f"Unknown model type for {name}: {model_type}")


def evaluate_experiment(name: str, train_df: pd.DataFrame, test_df: pd.DataFrame, model_type: str) -> dict[str, Any]:
    model = train_classifier(name, model_type)
    x_train = train_df[ATOM_COLUMNS]
    y_train = train_df["label"]
    x_test = test_df[ATOM_COLUMNS]
    y_test = test_df["label"]
    model.fit(x_train, y_train)
    preds = model.predict(x_test)
    row = make_eval_row(name, y_test.to_numpy(), preds)
    row["train_n"] = len(train_df)
    row["test_n"] = len(test_df)
    row["model"] = "Logistic Regression" if model_type == "lr" else "Random Forest"
    row["features"] = ", ".join(ATOM_COLUMNS)
    row["classification_report"] = classification_report(y_test, preds, target_names=["REAL", "FAKE"], digits=4)
    row["confusion_matrix"] = confusion_matrix(y_test, preds, labels=[0, 1]).tolist()
    return row


def run_decision_experiments(args: argparse.Namespace) -> None:
    df = features_dataframe()

    liar_train = df[(df["dataset"] == "liar") & (df["split"].isin(["train", "valid"]))].copy()
    liar_test = df[(df["dataset"] == "liar") & (df["split"] == "test")].copy()
    fnn_train = df[(df["dataset"] == "fakenewsnet") & (df["split"] == "train")].copy()
    fnn_test = df[(df["dataset"] == "fakenewsnet") & (df["split"] == "test")].copy()

    experiments = [
        ("LIAR atoms -> LIAR", liar_train, liar_test),
        ("LIAR atoms -> FakeNewsNet", liar_train, fnn_test),
        ("FakeNewsNet atoms -> FakeNewsNet", fnn_train, fnn_test),
    ]

    rows = []
    for name, train_df, test_df in experiments:
        if train_df.empty or test_df.empty:
            print(f"Skipping {name}: missing cached train or test features.")
            continue
        rows.append(evaluate_experiment(name, train_df, test_df, args.model_type))

    if not rows:
        raise RuntimeError("No experiments could run. Generate more feature cache rows first.")

    full_df = pd.DataFrame(rows)
    compact_cols = ["target", "model", "train_n", "test_n", "accuracy", "macro_f1", "real_recall", "fake_recall", "confusion_matrix"]
    compact = full_df[compact_cols].copy()
    for col in ["accuracy", "macro_f1", "real_recall", "fake_recall"]:
        compact[col] = compact[col].map(format_float)

    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    suffix = args.model_type
    full_df.to_csv(RESULTS_DIR / f"llm_reasoning_atoms_{suffix}_full_results.csv", index=False)
    compact.to_csv(RESULTS_DIR / f"llm_reasoning_atoms_{suffix}_compact_results.csv", index=False)

    lines = [
        "# LLM-Generated Reasoning Atoms: TELLER-Like Experiment",
        "",
        f"- Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}",
        f"- Feature cache: `{FEATURE_CACHE.relative_to(PROJECT_ROOT)}`",
        f"- Decision model: `{compact['model'].iloc[0]}`",
        "- LLM is used only to generate structured reasoning signals; it does not directly predict REAL/FAKE.",
        "- Label mapping: REAL=0, FAKE=1",
        "",
        "## Atom Features",
        "",
        *[f"- `{col}`" for col in ATOM_COLUMNS],
        "",
        "## Compact Results",
        "",
        dataframe_to_markdown(compact),
        "",
        "## Interpretation Notes",
        "",
        "- `LIAR atoms -> LIAR` is the in-domain check.",
        "- `LIAR atoms -> FakeNewsNet` is the cross-dataset transfer setting.",
        "- `FakeNewsNet atoms -> FakeNewsNet` is the target-domain upper-bound check using the same atom feature space.",
        "- This is a simplified TELLER-like setup: cognition-style atom generation is separated from the decision classifier.",
        "",
    ]

    for row in rows:
        lines.extend([
            f"## Classification Report: {row['target']}",
            "",
            "```text",
            row["classification_report"].strip(),
            "```",
            "",
        ])

    (RESULTS_DIR / f"llm_reasoning_atoms_{suffix}_report.md").write_text("\n".join(lines), encoding="utf-8")
    print(dataframe_to_markdown(compact))
    print(f"\nSaved results to: {RESULTS_DIR}")


def write_plan() -> None:
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    plan = [
        "# LLM-Generated Reasoning Atoms Experiment Plan",
        "",
        "This experiment is a lightweight TELLER-like design: an LLM generates structured cognition-style atoms, and a separate classifier makes the REAL/FAKE decision.",
        "",
        "## Features",
        "",
        *[f"- `{col}`" for col in ATOM_COLUMNS],
        "- `reason` is saved for auditability but is not used as a classifier input.",
        "",
        "## Experiments",
        "",
        "| Experiment | Training | Testing | Purpose |",
        "|---|---|---|---|",
        "| LIAR atoms -> LIAR | LIAR train+valid atom features | LIAR test atom features | In-domain check |",
        "| LIAR atoms -> FakeNewsNet | LIAR train+valid atom features | FakeNewsNet test atom features | Cross-dataset transfer |",
        "| FakeNewsNet atoms -> FakeNewsNet | FakeNewsNet train atom features | FakeNewsNet test atom features | Target-domain upper bound |",
        "",
        "## Suggested Pilot",
        "",
        "Start with a balanced small sample before full annotation:",
        "",
        "```powershell",
        "python notebooks/12_llm_reasoning_atoms_teller_like.py generate --provider deepseek --model deepseek-v4-flash --max-per-group 20",
        "python notebooks/12_llm_reasoning_atoms_teller_like.py train --model-type lr",
        "```",
        "",
        "Use `--provider openai --model gpt-4o-mini` or `--provider ollama --model <local-model>` as alternatives.",
        "",
    ]
    (RESULTS_DIR / "README.md").write_text("\n".join(plan), encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="LLM reasoning-atoms experiment for fake-news detection.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    generate = subparsers.add_parser("generate", help="Generate missing atom features into the JSONL cache.")
    generate.add_argument("--provider", choices=["openai", "deepseek", "ollama"], default="deepseek")
    generate.add_argument("--model", default="deepseek-v4-flash")
    generate.add_argument("--ollama-url", default="http://localhost:11434")
    generate.add_argument("--max-per-group", type=int, default=20, help="Balanced pilot size per dataset/split/label group. Omit for full data.")
    generate.add_argument("--seed", type=int, default=42)
    generate.add_argument("--sleep-seconds", type=float, default=0.2)
    generate.add_argument("--retries", type=int, default=3)
    generate.add_argument("--dry-run", action="store_true")

    train = subparsers.add_parser("train", help="Train/evaluate LR or RF on cached atom features.")
    train.add_argument("--model-type", choices=["lr", "rf"], default="lr")

    subparsers.add_parser("plan", help="Write the experiment plan README.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if args.command == "generate":
        write_plan()
        generate_missing_features(args)
    elif args.command == "train":
        write_plan()
        run_decision_experiments(args)
    elif args.command == "plan":
        write_plan()
        print(f"Wrote {RESULTS_DIR / 'README.md'}")


if __name__ == "__main__":
    main()
