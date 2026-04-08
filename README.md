# MSc Project — Cross-dataset Generalisation for Fake News Detection

**Supervisor:** Dr. Josephine Griffith  
**Student:** Boyu Lu

---

## Project overview

This project studies **cross-dataset generalisation for fake news / misinformation detection**, with a current focus on building and analysing strong baselines on the **LIAR** dataset before moving to cross-dataset experiments.

The overall goal is to understand:

- how model performance changes under dataset shift,
- why performance drops when moving across datasets,
- and whether simple adaptation strategies can help reduce that drop.

At the current stage, the project has established several **LIAR in-domain binary baselines**, which now provide the foundation for later cross-dataset work.

---

## Current project stage

The project is currently in the **baseline consolidation and transition stage**.

This means:

- the LIAR in-domain baseline line has already been established,
- stronger transformer baselines have been implemented and compared,
- the current priority is now to:
  - consolidate the results clearly,
  - expand the literature review,
  - write error analysis,
  - and prepare the later **cross-dataset / cross-domain** pipeline.

The project is **no longer** mainly focused on improving only the traditional sparse baseline.

---

## Current main conclusion

The current LIAR binary baseline results show the following progression:

| Model | Accuracy | Macro-F1 | Notes |
|---|---:|---:|---|
| TF-IDF + Logistic Regression | 0.6235 | 0.6005 | Main sparse baseline |
| BERT-base (3-seed mean) | 0.6369 ± 0.0028 | 0.6169 ± 0.0054 | Main unweighted neural baseline |
| BERT-base + weighted loss (3-seed mean) | 0.6404 ± 0.0078 | 0.6304 ± 0.0081 | Current primary model |
| RoBERTa-base (single run) | 0.6504 | 0.6262 | Comparison model |

### Current primary model

The current **primary model** is **BERT-base with weighted loss**.

This model is currently preferred because:

- it gives the **best mean Macro-F1** among the tested baselines,
- it improves over the unweighted BERT baseline,
- it improves **FAKE recall**,
- and it gives the best overall **class-balanced performance**.

RoBERTa currently achieves slightly higher single-run accuracy, but weighted BERT is more suitable as the main model because the project prioritises balanced performance rather than raw accuracy alone.

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
  Short narrative summary of project progress.

- `notes/clean_notes.md`  
  Explainable research notes, decisions, and open questions.

- `notebooks/`  
  Main experiment notebooks used in this project.
  - `01_liar_load.ipynb` — load and inspect the LIAR dataset
  - `02_tfidf_baseline.ipynb` — TF-IDF baseline experiments
  - `03_bert_baseline.ipynb` — BERT baseline
  - `04_bert_weighted_baseline.ipynb` — weighted BERT baseline
  - `05_roberta_baseline.ipynb` — RoBERTa baseline

- `results/`  
  Experiment outputs and evaluation summaries.
  - `baseline_results_summary.md` — short high-level summary of current results
  - `liar_baseline.md` — detailed LIAR baseline record

- `papers/reading_list.md`  
  Literature reading list.

- `papers/summaries/`  
  One-page summaries of selected papers.

---

## Working principles

- `tracking.md` is the main place for task status and evidence.
- `plans/` and `progress/` provide context, but do not replace `tracking.md`.
- Experimental results should be clearly recorded in `results/`.
- Notes should remain explainable and concise.
- The notebooks in this repository are the **user’s own working versions** and remain the primary implementation record for the dissertation.

---

## Update rules

- Every paper read → add it to `papers/reading_list.md` and create or update a summary in `papers/summaries/`
- Every few days → update `progress/progress_summary.md`
- Every week → refresh `plans/plan_next_2_weeks.md`
- After each meaningful experiment update → record results in `results/`
- When the project conclusion changes → synchronise `results/`, `progress/`, `plans/`, and `tracking.md`

---

## Current priorities

The current priorities are:

1. finalise and synchronise the baseline result documentation,
2. expand the literature review,
3. write error analysis for the weighted BERT model,
4. prepare the cross-dataset / cross-domain pipeline.

Optional additional experiments only if time allows:

- RoBERTa + weighted loss
- statement vs statement + context

---

## Implementation references

Some implementation ideas were informed by publicly available repositories related to fake news detection and the LIAR dataset:

- `https://github.com/tomtuamnuq/LIAR-Detect-Fake-News-Statement-Classification`
- `https://github.com/moscatena/Fake-News-Classification`

These repositories were used only as **implementation references**.

They do **not** replace the notebooks in this repository.  
All notebooks in this project are the **user’s own working versions** written specifically for this dissertation workflow.

---

## Current status summary

At the current stage of the project:

- the traditional sparse baseline has been completed,
- stronger transformer baselines have been implemented,
- weighted BERT is currently the main model,
- the project is ready to shift more attention toward:
  - interpretation,
  - literature review,
  - and the later cross-dataset stage.
