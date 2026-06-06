# -*- coding: utf-8 -*-
"""
Within-FakeNewsNet subpart transfer (PolitiFact <-> GossipCop), TF-IDF + class-weighted Logistic Regression.

Motivation (2026-06-04 supervisor meeting): FakeNewsNet minimal is used as one combined target.
The supervisor asked to look at its subparts separately and run small transfer experiments
between them (train on one subpart, test on another). The minimal release contains TWO source
domains: politifact and gossipcop. This script reports:
  - In-domain reference for each subpart (stratified 80/20 split, 5 seeds, mean +/- std).
  - Cross-subpart transfer in both directions (train all of A -> test all of B), deterministic.

Title text only; binary REAL(0)/FAKE(1). Mirrors the project's TF-IDF baseline conventions.
"""
import os, numpy as np, pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, f1_score, recall_score, confusion_matrix

ROOT = r"C:\Users\lby\Downloads\fake-news-projects\v2"
CSV = os.path.join(ROOT, "data", "fakenewsnet_minimal", "processed", "fakenewsnet_minimal_titles.csv")
OUTDIR = os.path.join(ROOT, "results", "fakenewsnet_subpart_transfer")
os.makedirs(OUTDIR, exist_ok=True)
SEEDS = [42, 52, 62, 72, 82]

df = pd.read_csv(CSV, usecols=["source", "y", "text"]).dropna(subset=["text"])
df["text"] = df["text"].astype(str)
pol = df[df.source == "politifact"].reset_index(drop=True)
gos = df[df.source == "gossipcop"].reset_index(drop=True)

def counts(d):
    return f"n={len(d)} REAL={int((d.y==0).sum())} FAKE={int((d.y==1).sum())}"
print("PolitiFact:", counts(pol))
print("GossipCop :", counts(gos))

def make_vec():
    return TfidfVectorizer(lowercase=True, ngram_range=(1,2), min_df=2,
                           sublinear_tf=True, strip_accents="unicode")

def fit_eval(Xtr, ytr, Xte, yte):
    vec = make_vec()
    Xtr_v = vec.fit_transform(Xtr); Xte_v = vec.transform(Xte)
    clf = LogisticRegression(max_iter=2000, class_weight="balanced", n_jobs=-1)
    clf.fit(Xtr_v, ytr)
    p = clf.predict(Xte_v)
    cm = confusion_matrix(yte, p, labels=[0,1])
    return dict(acc=accuracy_score(yte,p), mf1=f1_score(yte,p,average="macro"),
                real_rec=recall_score(yte,p,pos_label=0,zero_division=0),
                fake_rec=recall_score(yte,p,pos_label=1,zero_division=0), cm=cm)

rows = []

# In-domain references (5-seed stratified split)
for name, d in [("PolitiFact", pol), ("GossipCop", gos)]:
    accs=[]; mf1s=[]; rr=[]; fr=[]
    for s in SEEDS:
        Xtr,Xte,ytr,yte = train_test_split(d.text.values, d.y.values, test_size=0.2,
                                           stratify=d.y.values, random_state=s)
        r = fit_eval(Xtr,ytr,Xte,yte)
        accs.append(r["acc"]); mf1s.append(r["mf1"]); rr.append(r["real_rec"]); fr.append(r["fake_rec"])
    rows.append(dict(setting=f"In-domain {name} (5-seed 80/20)", train=name, test=name,
                     n_train=int(len(d)*0.8), n_test=int(len(d)*0.2),
                     acc=np.mean(accs), acc_std=np.std(accs), mf1=np.mean(mf1s), mf1_std=np.std(mf1s),
                     real_rec=np.mean(rr), fake_rec=np.mean(fr), cm=""))

# Cross-subpart transfer (deterministic: all of source -> all of target)
for sname, sdf, tname, tdf in [("PolitiFact", pol, "GossipCop", gos), ("GossipCop", gos, "PolitiFact", pol)]:
    r = fit_eval(sdf.text.values, sdf.y.values, tdf.text.values, tdf.y.values)
    rows.append(dict(setting=f"Transfer {sname} -> {tname}", train=sname, test=tname,
                     n_train=len(sdf), n_test=len(tdf),
                     acc=r["acc"], acc_std=0.0, mf1=r["mf1"], mf1_std=0.0,
                     real_rec=r["real_rec"], fake_rec=r["fake_rec"], cm=str(r["cm"].tolist())))

res = pd.DataFrame(rows)
res.to_csv(os.path.join(OUTDIR, "fnn_subpart_transfer_tfidf.csv"), index=False)

# markdown
def f(x): return f"{x:.4f}"
lines = ["# Within-FakeNewsNet Subpart Transfer (TF-IDF + weighted LR)", "",
         f"- Date: 2026-06-05", f"- PolitiFact: {counts(pol)}", f"- GossipCop: {counts(gos)}",
         "- Model: TF-IDF (1-2 gram, min_df=2, sublinear) + class-weighted Logistic Regression.",
         "- Binary REAL(0)/FAKE(1), title text only. In-domain rows are 5-seed 80/20 mean; transfer rows are deterministic (all source -> all target).",
         "", "| Setting | Train->Test | n_train | n_test | Accuracy | Macro-F1 | REAL recall | FAKE recall |",
         "|---|---|---:|---:|---:|---:|---:|---:|"]
for _,r in res.iterrows():
    acc = f(r.acc)+(f" (±{r.acc_std:.3f})" if r.acc_std>0 else "")
    mf1 = f(r.mf1)+(f" (±{r.mf1_std:.3f})" if r.mf1_std>0 else "")
    lines.append(f"| {r.setting} | {r.train}->{r.test} | {r.n_train} | {r.n_test} | {acc} | {mf1} | {f(r.real_rec)} | {f(r.fake_rec)} |")
open(os.path.join(OUTDIR,"fnn_subpart_transfer_tfidf.md"),"w",encoding="utf-8").write("\n".join(lines))
print("\n".join(lines))
print("\nSaved to", OUTDIR)
