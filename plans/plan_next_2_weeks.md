# Plan (Next 2 Weeks) — Baseline Improvement Focused (Ireland time / GMT)

> Note (for supervisor): The up-to-date task status and evidence links are maintained in `tracking.md` (single source of truth).  
> This file provides planning context only.

---

## Context

After the supervisor meeting on **2026-03-19**, the priority of the project has been updated.

The current LIAR baseline (**Version 1**) has already been completed, but the result is still relatively low and needs further investigation before moving on to stronger models such as BERT.

So, the next stage is not to move directly to a new model, but to first improve the traditional LIAR baseline and explain the reasons for the current performance.

---

## Current Baseline Status

Completed work so far:

- `notebooks/01_liar_load.ipynb`
  - LIAR train / valid / test splits loaded and inspected
- `notebooks/02_tfidf_baseline.ipynb`
  - TF-IDF + Logistic Regression baseline implemented
- `results/liar_baseline.md`
  - initial evaluation metrics recorded

Current Version 1 result:

- Task: binary classification
- Text field: `statement`
- Accuracy: `0.6196`
- Macro-F1: `0.5935`

Current binary mapping used in this project:

- REAL (0): `true`, `mostly-true`, `half-true`
- FAKE (1): `barely-true`, `false`, `pants-fire`

---

## Main Goal for the Next 2 Weeks

Improve the LIAR TF-IDF baseline and explain why Version 1 produced relatively low results.

This includes:

1. comparing Version 1 with the literature
2. improving preprocessing
3. checking TF-IDF parameter choices
4. using the validation split properly
5. updating the repository so that it clearly reflects the user's own working notebooks and results

---

# Week 1 (2026-03-19 to 2026-03-25)

## Task 1: Compare Version 1 with the literature

**Goal:** understand whether the current result is below typical LIAR baseline performance.

**Outputs:**
- find 2–3 papers or strong baseline references using LIAR
- record for each one:
  - task setting
  - label setting
  - model
  - reported metrics
- write a short comparison note in:
  - `results/liar_baseline.md`
  - or `progress/progress_summary.md`

**Reason:**
This helps explain how far the current Version 1 result is from existing work and gives a clearer target for improvement.

---

## Task 2: Improve preprocessing for the traditional baseline

**Goal:** test whether stronger preprocessing improves performance.

**Changes to compare:**
- basic cleanup
- lowercasing
- stopword removal
- stemming or lemmatization

**Outputs:**
- update `notebooks/02_tfidf_baseline.ipynb`
- compare preprocessing settings on `valid.tsv`
- record the comparison results in `results/liar_baseline.md`

**Reason:**
The supervisor noted that Version 1 preprocessing was too limited for a traditional method such as TF-IDF + Logistic Regression.

---

## Task 3: Use the validation split properly

**Goal:** make model selection more systematic.

**Outputs:**
- use `train.tsv` for training
- use `valid.tsv` to compare candidate settings
- keep `test.tsv` for final evaluation only

**Reason:**
The supervisor specifically pointed out that Version 1 did not make proper use of the validation split.

---

## Task 4: Check TF-IDF parameter choices

**Goal:** understand and justify the feature settings used in the baseline.

**Parameters to review:**
- `ngram_range`
- `min_df`
- `max_df`

**Outputs:**
- test several reasonable TF-IDF settings in `notebooks/02_tfidf_baseline.ipynb`
- write short notes explaining:
  - what each parameter means
  - why it matters
  - what effect it has on the features and results

**Reason:**
The supervisor asked for a clearer explanation of these choices and whether they may be contributing to the low result.

---

# Week 2 (2026-03-26 to 2026-04-01)

## Task 5: Finalise LIAR baseline Version 2

**Goal:** produce an improved and better justified baseline.

**Outputs:**
- select the best preprocessing + TF-IDF setup using validation results
- retrain using the selected setup
- evaluate once on the test split
- record:
  - Accuracy
  - Macro-F1
  - confusion matrix
  - classification report
- compare Version 2 with Version 1

Files:
- `notebooks/02_tfidf_baseline.ipynb`
- `results/liar_baseline.md`

---

## Task 6: Update repository structure and consistency

**Goal:** make the repository easier for the supervisor to read and ensure that it reflects the user's real work.

**Outputs:**
- ensure the notebooks in `notebooks/` are the user's own working versions
- keep external GitHub repositories only as implementation references
- list external references in `README.md`
- update:
  - `tracking.md`
  - `progress/progress_summary.md`
  - `results/liar_baseline.md`

**Reason:**
The supervisor noted that the repository should primarily show the user's own notebook versions, not just external GitHub code.

---

## Task 7: Prepare the next supervisor update

**Goal:** be ready to explain the progress clearly at the next meeting.

**Prepare to report:**
- what Version 1 did
- why Version 1 was relatively low
- what was changed in Version 2
- whether the improved result is closer to the literature
- what should come next after the improved baseline

**Outputs:**
- short written summary in `progress/progress_summary.md`
- updated evidence links in `tracking.md`

---

## Expected Deliverables by the End of This Period

By the end of this two-week period, the project should have:

1. a completed LIAR baseline Version 2
2. a Version 1 vs Version 2 comparison
3. a short literature comparison for LIAR baseline results
4. clearer justification for preprocessing and TF-IDF parameters
5. a cleaner repository that shows the user's own notebook workflow more clearly

---

## Notes on Scope

During this period, the main focus is still the LIAR baseline improvement stage.

Work on stronger baselines such as BERT, or later cross-dataset experiments, should begin only after the traditional baseline is improved and the current low result is better understood.
