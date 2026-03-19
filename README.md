# MSc Project — Cross-dataset Generalisation for Fake News Detection

**Supervisor:** Dr. Josephine Griffith  
**Student:** Boyu Lu

---

## Project overview

This project studies **cross-dataset generalisation for fake news / misinformation detection**, focusing on how performance changes under dataset shift across benchmark datasets such as **LIAR** and **FakeNewsNet**.

The overall goal is to understand how well models trained on one dataset transfer to another, what causes performance drop under distribution shift, and whether lightweight adaptation strategies can help reduce that drop.

---

## Current project stage

The project is currently in the **baseline development and improvement stage**.

At this stage, the priority is to:

- establish a clear in-domain baseline on **LIAR**
- improve and better justify the traditional baseline
- compare results with previous work
- prepare for later cross-dataset experiments

The current focus is **not** to move directly to stronger models, but to first improve the LIAR baseline and explain the current performance.

---

## Research Questions (draft)

- **RQ1:** How much does performance drop when training on Dataset A and testing on Dataset B?
- **RQ2:** What dataset differences (text style, label definition, topic/source) explain the drop?
- **RQ3:** Can lightweight adaptation (e.g., continued pretraining on target unlabeled text) reduce the drop?

---

## Datasets (draft)

- **LIAR**
- **FakeNewsNet**

---

## Repository structure

- `tracking.md`  
  Main project tracker. This is the **single source of truth** for current task status and evidence links.

- `plans/plan_next_2_weeks.md`  
  Short-term planning context.

- `progress/progress_summary.md`  
  Short narrative summary of progress.

- `notes/clean_notes.md`  
  Explainable research notes, decisions, and open questions.

- `notebooks/`  
  Experiment notebooks used in this project.

  - `01_liar_load.ipynb` — load and inspect the LIAR dataset
  - `02_tfidf_baseline.ipynb` — LIAR TF-IDF baseline experiments

- `results/`  
  Experiment outputs and evaluation results.

  - `liar_baseline.md` — LIAR baseline results and comparisons

- `papers/reading_list.md`  
  Literature reading list.

- `papers/summaries/`  
  One-page summaries of selected papers.

---

## Working principles

- `tracking.md` is the main place for task status and evidence.
- `plans/` and `progress/` provide context, but do not replace `tracking.md`.
- Experimental results should be recorded clearly in `results/`.
- Notes should remain explainable and concise.

---

## Update rule (for myself)

- Every paper read → add it to `reading_list.md` and create a summary in `papers/summaries/`
- Every few days → update `progress/progress_summary.md`
- Every week → refresh `plans/` with dates and deliverables
- After each meaningful experiment update → record results in `results/`

---

## Implementation References

Some implementation ideas were informed by publicly available repositories related to fake news detection and the LIAR dataset:

- `https://github.com/tomtuamnuq/LIAR-Detect-Fake-News-Statement-Classification`
- `https://github.com/moscatena/Fake-News-Classification`

These repositories were used only as **implementation references**.

The notebooks in this repository are the **user’s own working versions** written specifically for this dissertation workflow.
