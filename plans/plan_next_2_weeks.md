# Plan (Next 2 Weeks) — Post-Baseline Consolidation Focused (Ireland time)

> Note (for supervisor): the up-to-date task status and evidence links are maintained in `tracking.md` as the single source of truth.  
> This file provides planning context only.

---

## Context

The project has now moved beyond the traditional sparse-baseline stage.

The LIAR in-domain binary baseline line is now established across several models:

- **TF-IDF + Logistic Regression**
- **BERT-base**
- **BERT-base + weighted loss**
- **RoBERTa-base**

At the current stage, the strongest main model is **weighted BERT**, because it gives the best average **Macro-F1** and the best overall class-balanced performance among the tested baselines.

This means the main priority for the next two weeks is **no longer** to keep tuning the traditional baseline.  
Instead, the focus should now shift to:

1. consolidating the current baseline results,
2. expanding the literature review,
3. writing error analysis,
4. preparing the next-stage **cross-dataset / cross-domain** pipeline.

---

## Current Baseline Status

Completed work so far:

- `notebooks/01_liar_load.ipynb`
  - LIAR train / valid / test splits loaded and inspected

- `notebooks/02_tfidf_baseline.ipynb`
  - TF-IDF + Logistic Regression sparse baseline completed

- `notebooks/03_bert_baseline.ipynb`
  - unweighted BERT baseline completed on GPU

- `notebooks/04_bert_weighted_baseline.ipynb`
  - weighted-loss BERT baseline completed

- `notebooks/05_roberta_baseline.ipynb`
  - RoBERTa baseline completed

Main current results:

- **TF-IDF + Logistic Regression**
  - Accuracy: `0.6235`
  - Macro-F1: `0.6005`

- **BERT-base (3-seed mean)**
  - Accuracy: `0.6369 ± 0.0028`
  - Macro-F1: `0.6169 ± 0.0054`

- **BERT-base + weighted loss (3-seed mean)**
  - Accuracy: `0.6404 ± 0.0078`
  - Macro-F1: `0.6304 ± 0.0081`

- **RoBERTa-base (single run)**
  - Accuracy: `0.6504`
  - Macro-F1: `0.6262`

Current main model:
- **weighted BERT**

Reason:
- best mean Macro-F1 among tested baselines
- better FAKE recall than unweighted BERT and RoBERTa
- more suitable for class-balanced fake news detection than accuracy-only selection

---

## Main Goal for the Next 2 Weeks

Use the current LIAR baseline results as a stable foundation and shift the project toward thesis-ready analysis and next-stage design.

This includes:

1. finalising and synchronising the current result documentation,
2. expanding the literature review beyond the current small set of papers,
3. writing error analysis for the weighted BERT model,
4. preparing the cross-dataset / cross-domain pipeline,
5. keeping extra model experiments optional rather than central.

---

# Week 1 (2026-04-09 to 2026-04-15)

## Task 1: Finalise baseline documentation across the repository

**Goal:** make the repository internally consistent and clearly reflect the current main conclusion.

**Files to synchronise:**
- `results/baseline_results_summary.md`
- `results/liar_baseline.md`
- `progress/progress_summary.md`
- `tracking.md`
- `notebooks/README.md`
- root `README.md`

**Outputs:**
- all files updated to reflect:
  - TF-IDF baseline completed
  - BERT baseline completed
  - weighted BERT as the current primary model
  - RoBERTa as a comparison model
- remove outdated “next step” language that still treats LinearSVC or sparse-model tuning as the main direction

**Reason:**
The experimental line has progressed much faster than the written project record.  
This now needs to be cleaned up so the repository is readable for the supervisor and usable for dissertation writing.

---

## Task 2: Expand the literature review

**Goal:** strengthen the related-work section so it matches the current experimental progress.

**Outputs:**
- extend `papers/reading_list.md`
- add or finalise more paper summaries in `papers/summaries/`
- make sure the literature review includes:
  - LIAR dataset background
  - transformer baselines for fake news detection
  - model-choice justification for BERT / RoBERTa
  - cross-dataset or generalisation discussion where relevant

**Minimum target for this period:**
- move beyond the current small set and build a more credible paper base for the thesis

**Reason:**
The supervisor explicitly noted that the literature review was still too limited.  
Now that the model results are stronger, the literature review needs to catch up.

---

## Task 3: Write error analysis for weighted BERT

**Goal:** move from raw performance numbers to interpretation.

**Focus:**
- false positives
- false negatives
- remaining FAKE-class errors
- patterns in short statements that are still difficult for the model

**Outputs:**
- collect representative error examples from the test split
- write short analysis notes that explain:
  - what kinds of statements are still misclassified
  - why FAKE recall improved relative to unweighted BERT
  - why class balance is still not perfect

**Files to update:**
- `results/liar_baseline.md`
- optionally `notes/clean_notes.md`

**Reason:**
The thesis needs explanation, not only metrics.  
Weighted BERT is especially suitable for error analysis because its improvement is interpretable.

---

# Week 2 (2026-04-16 to 2026-04-22)

## Task 4: Prepare the cross-dataset / cross-domain pipeline

**Goal:** begin the next stage of the project after the LIAR in-domain baseline line.

**Outputs:**
- define the next experimental pipeline beyond LIAR in-domain evaluation
- identify which dataset(s) will be used in the next stage
- outline the intended train / validation / test logic for cross-dataset experiments
- record the design clearly in:
  - `tracking.md`
  - `plans/plan_next_2_weeks.md`
  - `progress/progress_summary.md`

**Reason:**
The supervisor previously indicated that stronger models should be established first, and the cross part should follow.  
That condition is now satisfied, so the next planning step should begin.

---

## Task 5: Prepare supervisor-facing update files

**Goal:** make the next supervisor update easy to read in advance.

**Outputs:**
- decide which files should be sent to the supervisor before the next meeting
- make sure those files are clean and up to date
- prioritise:
  - `results/baseline_results_summary.md`
  - `results/liar_baseline.md`
  - `progress/progress_summary.md`
  - `tracking.md`

**Reason:**
The supervisor asked to be told which files to review before the next meeting.

---

## Task 6: Keep additional model work optional

**Goal:** avoid spending too much time on small extra variations unless they clearly add thesis value.

**Optional experiments only if time allows:**
- `RoBERTa + weighted loss`
- `statement` vs `statement + context`

**Reason:**
The current main bottleneck is no longer whether the project has a strong enough baseline.  
The bigger need now is analysis, literature coverage, and next-stage pipeline design.

---

## Expected Deliverables by the End of This Period

By the end of this two-week period, the project should have:

1. a fully synchronised repository record of the current LIAR baselines,
2. a clearer and expanded literature review,
3. a written error analysis for the weighted BERT model,
4. an initial design for the cross-dataset / cross-domain stage,
5. a clean set of files ready to share with the supervisor.

---

## Notes on Scope

During this period, the main focus is **not** to keep pushing small model improvements.

The main focus is to make the current results thesis-ready and to prepare the next research stage.

Additional model experiments are allowed only if they clearly support one of these goals:
- stronger interpretation,
- stronger comparison,
- or better preparation for the next-stage pipeline.
