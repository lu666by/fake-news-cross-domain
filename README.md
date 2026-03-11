# MSc Project — Cross-dataset Generalisation for Fake News Detection

Supervisor: Dr. Josephine Griffith  
Student: Boyu Lu

---

## Project idea (1–2 sentences)

This project studies **cross-dataset generalisation for fake news / misinformation detection**, focusing on domain shift between datasets (e.g., LIAR vs. FakeNewsNet) and simple robustness strategies.

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
  Main project tracker (task status + evidence links).

- `plans/plan_next_2_weeks.md`  
  Short-term implementation plan.

- `progress/progress_summary.md`  
  Narrative summary of project progress.

- `notes/clean_notes.md`  
  Explainable research notes and decisions.

- `notebooks/`  
  Experiment notebooks.

  - `01_liar_load.ipynb` — load and inspect LIAR dataset  
  - `02_tfidf_baseline.ipynb` — TF-IDF baseline experiment

- `results/`  
  Experiment outputs and evaluation results.

  - `liar_baseline.md` — baseline experiment metrics

- `papers/reading_list.md`  
  Literature reading list.

- `papers/summaries/`  
  One-page summaries of key papers.

---

## Update rule (for myself)

- Every paper read → add to `reading_list.md` and create a summary in `papers/summaries/`
- Every 2–3 days → update `progress/progress_summary.md`
- Every week → refresh `plans/` with dates and deliverables

---

## Code references

Some implementation ideas were informed by publicly available repositories related to fake news detection and the LIAR dataset:

- https://github.com/tomtuamnuq/LIAR-Detect-Fake-News-Statement-Classification
- https://github.com/moscatena/Fake-News-Classification

These repositories were used only as **implementation references**.  
All notebooks in this project were written specifically for this dissertation workflow.
