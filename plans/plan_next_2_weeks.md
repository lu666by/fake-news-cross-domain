# Plan (Next 2 Weeks) — Implementation-focused (Ireland time / GMT)

> Note (for supervisor): The up-to-date plan and completion status are maintained in `tracking.md` (single source of truth).  
> This file provides background planning context only.

---

## Context
- I returned to Ireland on **2026-03-04**.
- Due to family medical appointments during that week, implementation work was scheduled to begin from **2026-03-05**.

---

## Goals (deliverables)

By **2026-03-12**, the following implementation milestones should be completed:

1. **Project tracking structure**
   - `tracking.md` used as the single place that records task status and evidence links.

2. **Initial LIAR dataset experiments**
   - `notebooks/01_liar_load.ipynb`  
     Load and inspect the LIAR dataset.

   - `notebooks/02_tfidf_baseline.ipynb`  
     Run a TF-IDF baseline experiment.

   - `results/liar_baseline.md`  
     Record evaluation metrics (Accuracy, Macro-F1, Confusion Matrix).

3. **Clean research notes**
   - `notes/clean_notes.md`
   - Ensure each note or question can be clearly explained.

---

# Week 1 (2026-03-05 to 2026-03-08)

## Day 1 (2026-03-05)
**Task:** Finalise single-entry tracking setup

**Outputs:**
- Ensure `tracking.md` is the only file that records task status.
- Add short pointer notes at the top of:
  - `plans/plan_next_2_weeks.md`
  - `progress/progress_summary.md`

---

## Day 2 (2026-03-06)

**Task:** Clean research notes

**Outputs:**
- Create/update `notes/clean_notes.md`
- Apply the **3-sentence test** to each item:

1. What it means  
2. Why it matters  
3. Next step

Notes that cannot be clearly explained are removed or rewritten.

---

## Day 3–Day 4 (2026-03-07 to 2026-03-08)

**Task:** Begin LIAR dataset implementation

**Outputs:**

`notebooks/01_liar_load.ipynb`

The notebook performs:

- loading `train.tsv`, `valid.tsv`, `test.tsv`
- printing dataset shapes
- showing label distribution
- printing several example statements

This step confirms that the dataset is correctly prepared for later experiments.

---

# Week 2 (2026-03-08 to 2026-03-12)

## Day 5–Day 7 (2026-03-08 to 2026-03-10)

**Task:** Implement TF-IDF baseline experiment (LIAR in-domain)

**Outputs:**

`notebooks/02_tfidf_baseline.ipynb`

The notebook includes:

- TF-IDF text representation
- Logistic Regression classifier  
- optional comparison with Linear SVM

Evaluation metrics:

- Accuracy
- Macro-F1
- Confusion Matrix

Results are recorded in:

`results/liar_baseline.md`

---

## Day 8–Day 9 (2026-03-11 to 2026-03-12)

**Task:** Review and polish project materials

**Outputs:**

1. Update `tracking.md`
   - ensure task status is accurate
   - ensure evidence links are correct

2. Review `notes/clean_notes.md`
   - confirm that each note is clearly explainable

3. Write a short update in `progress/progress_summary.md`
   (1–2 paragraphs)

The update should summarise:

- what was completed
- what the next steps will be

---

## Literature reading (lightweight)

Literature reading will be kept minimal during this implementation period.

New paper summaries will only be added if they directly support the implementation tasks.

If a new summary is added:

- include an **"LLM Prompt(s)" section**
- save the file under:

`papers/summaries/`
