# Plan (Next 2 Weeks) — Implementation-focused (Ireland time / GMT)

> Note (for supervisor): The up-to-date plan + progress is maintained in `tracking.md` (single source of truth).
> This file provides background detail only.

## Context
- I will be travelling back to Ireland on **2026-03-04**.
- Due to family medical appointments this week, I shifted the implementation tasks to start from **2026-03-05**.

## Goals (deliverables)
By **2026-03-12** (approx. two weeks after return):
1) A clean and readable tracker (`tracking.md`) showing what is planned vs done (with evidence links).
2) Start coding with **LIAR**:
   - `notebooks/01_liar_load.ipynb` (load + inspect)
   - `notebooks/02_tfidf_baseline.ipynb` (TF-IDF baseline)
   - `results/liar_baseline.md` (metrics recorded)
3) Clean notes so that all questions/risks are explainable:
   - `notes/clean_notes.md`

---

## Week 1 (2026-03-05 to 2026-03-08)

### Day 1 (2026-03-05)
- Task: Finish “single entry” tracking setup
- Output:
  - Ensure `tracking.md` is the only place that tracks status
  - Add short pointers at the top of:
    - `plans/plan_next_2_weeks.md`
    - `progress/progress_summary.md`

### Day 2 (2026-03-06)
- Task: Clean notes (only keep explainable items)
- Output:
  - Create/update `notes/clean_notes.md`
  - Apply “3-sentence test” for each note/question:
    - What it means / Why it matters / Next step

### Day 3–Day 4 (2026-03-07 to 2026-03-08)
- Task: Start LIAR coding — load + inspect dataset
- Output:
  - `notebooks/01_liar_load.ipynb` with:
    - load train/valid/test
    - dataset shapes
    - label counts
    - 3 sample statements

---

## Week 2 (2026-03-08 to 2026-03-12)

### Day 5–Day 7 (2026-03-08 to 2026-03-10)
- Task: TF-IDF baseline + metrics (LIAR in-domain)
- Output:
  - `notebooks/02_tfidf_baseline.ipynb`:
    - TF-IDF + Logistic Regression (optional: Linear SVM)
    - report Accuracy + Macro-F1 + Confusion Matrix
  - Fill `results/liar_baseline.md` with the results

### Day 8–Day 9 (2026-03-11 to 2026-03-12)
- Task: Review & polish (make it supervisor-readable)
- Output:
  - Update `tracking.md` statuses + evidence links
  - Ensure `notes/clean_notes.md` contains only items I can explain clearly
  - Short update in `progress/progress_summary.md` (1–2 paragraphs):
    - what was done
    - what is next

---

## Literature reading (lightweight, optional)
- Keep literature work minimal during these two weeks.
- Only add new paper summaries if they directly support the implementation tasks.
- If any new summary is added, include:
  - “LLM Prompt(s)” section
  - file saved under `papers/summaries/`
