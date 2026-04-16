# MSc Project — Cross-dataset Generalisation for Fake News Detection

**Supervisor:** Dr. Josephine Griffith  
**Student:** Boyu Lu

---

## Project overview

This project studies **cross-dataset generalisation for fake news / misinformation detection**.

The current work focuses on building and analysing strong **LIAR in-domain binary baselines** before moving to the later **cross-dataset / cross-domain** stage.

The overall goal is to understand:

- how model performance changes under dataset shift,
- why performance drops across datasets,
- and whether simple adaptation strategies can help reduce that drop.

---

## Current project stage

The project is currently in the **baseline consolidation and transition stage**.

This means:

- the LIAR in-domain baseline line has already been established,
- the main transformer baselines have been stabilised with **5-run results**,
- and the current priority is now:
  - to consolidate the results clearly,
  - to expand the literature review,
  - to write thesis-ready error analysis,
  - and to prepare the later **cross-dataset / cross-domain** pipeline.

The project is no longer mainly focused on improving only the traditional sparse baseline.

---

## Current main conclusion

The current LIAR binary baseline results are:

| Model | Accuracy | Macro-F1 | Notes |
|---|---:|---:|---|
| TF-IDF + Logistic Regression | 0.6235 | 0.6005 | Main sparse baseline |
| BERT-base (5-run mean) | 0.6425 ± 0.0095 | 0.6231 ± 0.0122 | Main unweighted neural baseline |
| BERT-base + weighted loss (5-run mean) | 0.6412 ± 0.0065 | 0.6322 ± 0.0090 | Stronger FAKE recall |
| RoBERTa-base + weighted loss (5-run mean) | 0.6522 ± 0.0074 | 0.6396 ± 0.0080 | Current strongest overall model |

### Current model interpretation

- **Current strongest overall model:** **RoBERTa-base + weighted loss**
- **Current strongest FAKE-recall comparison model:** **BERT-base + weighted loss**

This means the project now shows a useful trade-off:

- **weighted BERT** is stronger on **FAKE recall**
- **weighted RoBERTa** is stronger on **overall performance**

---

## Current task setting

### Dataset
- **LIAR**

### Evaluation setting
- **in-domain (LIAR → LIAR)**

### Input text
- **statement**

### Binary mapping
- **REAL (0):** `true`, `mostly-true`, `half-true`
- **FAKE (1):** `barely-true`, `false`, `pants-fire`

### Split sizes
- Train: 10240
- Valid: 1284
- Test: 1267

---

## Repository structure

- `tracking.md`  
  Main project tracker. This is the **single source of truth** for task status and evidence links.

- `plans/plan_next_2_weeks.md`  
  Short-term planning context.

- `progress/progress_summary.md`  
  Short weekly narrative update.

- `notes/clean_notes.md`  
  Explainable research notes, decisions, and open questions.

- `notebooks/`  
  Main experiment notebooks and scripts used in this project.
  - `01_liar_load.ipynb` — load and inspect the LIAR dataset
  - `02_tfidf_baseline.ipynb` — TF-IDF baseline
  - `03_bert_baseline.ipynb` — unweighted BERT baseline
  - `04_bert_weighted_baseline.ipynb` — weighted BERT baseline
  - `05_roberta_baseline.ipynb` — unweighted RoBERTa baseline
  - `06_roberta_weighted_baseline.ipynb` — weighted RoBERTa baseline
  - `07_roberta_weighted_context_comparison.py` — statement vs statement + context comparison
  - `08_roberta_weighted_threshold_tuning.py` — threshold tuning for weighted RoBERTa

- `results/`  
  Experiment outputs and evaluation summaries.
  - `baseline_results_summary.md` — short high-level summary of current results
  - `liar_baseline.md` — detailed LIAR baseline record

- `papers/reading_list.md`  
  Literature reading list.

- `papers/summaries/`  
  One-page summaries of selected papers.

---

## Current priorities

The current priorities are:

1. finalise and synchronise the baseline result documentation,
2. expand the literature review,
3. turn the current error analysis into thesis-ready writing,
4. prepare the cross-dataset / cross-domain pipeline.

---

## Implementation references

Some implementation ideas were informed by publicly available repositories related to fake news detection and the LIAR dataset:

- `https://github.com/tomtuamnuq/LIAR-Detect-Fake-News-Statement-Classification`
- `https://github.com/moscatena/Fake-News-Classification`

These repositories were used only as **implementation references**.

They do **not** replace the notebooks and scripts in this repository.  
The files in this project remain the user’s own working versions written specifically for this dissertation workflow.
