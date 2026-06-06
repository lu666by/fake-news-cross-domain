# -*- coding: utf-8 -*-
"""
Within-FakeNewsNet subpart transfer with weighted RoBERTa (single seed, GPU).
Confirms whether the TF-IDF cross-subpart pattern (notebook 14) also holds for the transformer baseline.

Reuses the proven training/eval helpers from notebook 13 (which imports notebook 10).
Settings: weighted RoBERTa (roberta-base), max_len 128, batch 16, 3 epochs, checkpoint by valid Macro-F1.
"""
from __future__ import annotations
import importlib.util, time, types
from datetime import datetime
from pathlib import Path
import pandas as pd, torch
from sklearn.model_selection import train_test_split
from transformers import AutoModelForSequenceClassification, AutoTokenizer

from cross_dataset_utils import find_project_root, load_fakenewsnet_minimal, format_float

ROOT = find_project_root()
nb13_path = ROOT / "notebooks" / "13_intermediate_finetuning_fakenewsnet.py"
spec = importlib.util.spec_from_file_location("nb13", nb13_path)
nb13 = importlib.util.module_from_spec(spec); spec.loader.exec_module(nb13)

set_seed = nb13.set_seed
make_dataloader = nb13.make_dataloader
compute_class_weights = nb13.compute_class_weights
train_with_best_checkpoint = nb13.train_with_best_checkpoint
evaluate_model = nb13.evaluate_model
from liar_utils import ID2LABEL, evaluate_predictions
from sklearn.metrics import recall_score

OUTDIR = ROOT / "results" / "fakenewsnet_subpart_transfer"
OUTDIR.mkdir(parents=True, exist_ok=True)
MODEL = "roberta-base"
SEED = 42
args = types.SimpleNamespace(max_length=128, eval_batch_size=64, weight_decay=0.01, warmup_ratio=0.1)
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print("Device:", device, torch.cuda.get_device_name(0) if torch.cuda.is_available() else "", flush=True)

fnn = load_fakenewsnet_minimal(ROOT / "data" / "fakenewsnet_minimal" / "raw")
pol = fnn[fnn.source == "politifact"].reset_index(drop=True)
gos = fnn[fnn.source == "gossipcop"].reset_index(drop=True)
tok = AutoTokenizer.from_pretrained(MODEL)

def fresh_model():
    m = AutoModelForSequenceClassification.from_pretrained(
        MODEL, num_labels=2, id2label=ID2LABEL,
        label2id={v: k for k, v in ID2LABEL.items()})
    return m.to(device)

def train_eval(train_df, valid_df, test_df, stage):
    set_seed(SEED)
    m = fresh_model()
    w = compute_class_weights(train_df, device)
    train_with_best_checkpoint(m, train_df, valid_df, "text", tok, device, args,
                               3, 2e-5, 16, w, stage)
    test_loader = make_dataloader(test_df, "text", tok, args.max_length, args.eval_batch_size, shuffle=False)
    met = evaluate_model(m, test_loader, device)
    rr, fr = recall_score(met["labels"], met["preds"], labels=[0, 1], average=None, zero_division=0)
    del m
    if torch.cuda.is_available(): torch.cuda.empty_cache()
    return dict(stage=stage, test_n=len(met["labels"]), accuracy=met["accuracy"],
                macro_f1=met["macro_f1"], real_recall=rr, fake_recall=fr,
                confusion_matrix=met["confusion_matrix"].tolist())

rows = []
t0 = time.time()
# in-domain references (80/10/10-ish: split test 0.2, then valid 0.2 of remainder)
for name, d in [("PolitiFact", pol), ("GossipCop", gos)]:
    tr_va, te = train_test_split(d, test_size=0.2, random_state=SEED, stratify=d.y)
    tr, va = train_test_split(tr_va, test_size=0.2, random_state=SEED, stratify=tr_va.y)
    print(f"\n=== In-domain {name}: train={len(tr)} valid={len(va)} test={len(te)} ===", flush=True)
    r = train_eval(tr.reset_index(drop=True), va.reset_index(drop=True), te.reset_index(drop=True), f"in_domain_{name}")
    r["setting"] = f"In-domain {name}"; rows.append(r)

# cross-subpart transfer: train on all of source (small valid split for checkpoint), test on all of target
for sname, sdf, tname, tdf in [("PolitiFact", pol, "GossipCop", gos), ("GossipCop", gos, "PolitiFact", pol)]:
    tr, va = train_test_split(sdf, test_size=0.15, random_state=SEED, stratify=sdf.y)
    print(f"\n=== Transfer {sname}->{tname}: train={len(tr)} valid={len(va)} test={len(tdf)} ===", flush=True)
    r = train_eval(tr.reset_index(drop=True), va.reset_index(drop=True), tdf.reset_index(drop=True), f"transfer_{sname}_to_{tname}")
    r["setting"] = f"Transfer {sname} -> {tname}"; rows.append(r)

res = pd.DataFrame(rows)
res.to_csv(OUTDIR / "fnn_subpart_transfer_roberta_seed42.csv", index=False)
lines = ["# Within-FakeNewsNet Subpart Transfer (weighted RoBERTa, seed 42)", "",
         f"- Date: {datetime.now():%Y-%m-%d %H:%M}", f"- Model: {MODEL}, class-weighted, max_len 128, batch 16, 3 epochs, checkpoint by valid Macro-F1.",
         f"- Single seed ({SEED}); title text only; REAL(0)/FAKE(1). In-domain = 64/16/20 split; transfer = train all source -> test all target.",
         f"- Total runtime: {(time.time()-t0)/60:.1f} min.", "",
         "| Setting | Accuracy | Macro-F1 | REAL recall | FAKE recall |",
         "|---|---:|---:|---:|---:|"]
for _, r in res.iterrows():
    lines.append(f"| {r.setting} | {format_float(r.accuracy)} | {format_float(r.macro_f1)} | {format_float(r.real_recall)} | {format_float(r.fake_recall)} |")
(OUTDIR / "fnn_subpart_transfer_roberta_seed42.md").write_text("\n".join(lines), encoding="utf-8")
print("\n".join(lines)); print("\nSaved to", OUTDIR, flush=True)
