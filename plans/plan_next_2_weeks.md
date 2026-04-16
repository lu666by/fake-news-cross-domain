# Plan (Next 2 Weeks) — Post-Baseline Consolidation Focused (Ireland time)

> Note (for supervisor): the up-to-date task status and evidence links are maintained in `tracking.md` as the single source of truth.  
> This file provides planning context only.

---

## Context

The project has now moved well beyond the traditional sparse-baseline stage.

The LIAR in-domain binary baseline line is now established across several models:

- **TF-IDF + Logistic Regression**
- **BERT-base**
- **BERT-base + weighted loss**
- **RoBERTa-base + weighted loss**

The current comparison is now based on **more stable 5-run results** rather than only 1 or 3 runs.

At the current stage:

- **weighted RoBERTa** is the strongest **overall** model,
- **weighted BERT** remains important because it gives stronger **FAKE recall**,
- and the most direct low-cost follow-up ideas have already been tested:
  - naive context concatenation
  - threshold tuning

Those follow-up checks did **not** improve the current result, which suggests that the model line is now strong enough for the current phase of the project.

This means the main priority for the next two weeks is **no longer** broad model exploration.  
Instead, the focus should now shift to:

1. consolidating the current baseline results,
2. expanding the literature review,
3. writing thesis-ready error analysis,
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
  - unweighted RoBERTa baseline completed

- `notebooks/06_roberta_weighted_baseline.ipynb`
  - weighted RoBERTa baseline completed

- `notebooks/07_roberta_weighted_context_comparison.py`
  - statement-only vs statement + context comparison completed

- `notebooks/08_roberta_weighted_threshold_tuning.py`
  - threshold tuning check completed

### Main current results

- **TF-IDF + Logistic Regression**
  - Accuracy: `0.6235`
  - Macro-F1: `0.6005`

- **BERT-base (5-run mean)**
  - Accuracy: `0.6425 ± 0.0095`
  - Macro-F1: `0.6231 ± 0.0122`

- **BERT-base + weighted loss (5-run mean)**
  - Accuracy: `0.6412 ± 0.0065`
  - Macro-F1: `0.6322 ± 0.0090`
  - REAL recall: `0.7048 ± 0.0292`
  - FAKE recall: `0.5591 ± 0.0447`

- **RoBERTa-base + weighted loss (5-run mean)**
  - Accuracy: `0.6522 ± 0.0074`
  - Macro-F1: `0.6396 ± 0.0080`
  - REAL recall: `0.7443 ± 0.0153`
  - FAKE recall: `0.5335 ± 0.0199`

### Current model interpretation

- **Current strongest overall model:** weighted RoBERTa
- **Current strongest FAKE-recall comparison model:** weighted BERT

This distinction is important because the current thesis line is no longer only about which model has the highest score, but also about how the models differ in class balance and decision behaviour.

---

## Main Goal for the Next 2 Weeks

Use the current LIAR baseline line as a stable foundation and shift the project toward thesis-ready analysis and next-stage design.

This includes:

1. finalising and synchronising the current result documentation,
2. expanding the literature review beyond the current small set of papers,
3. writing the current error analysis into a thesis-ready form,
4. preparing the cross-dataset / cross-domain pipeline,
5. keeping extra model work non-central unless it clearly supports the dissertation.

---

# Week 1 (2026-04-16 to 2026-04-22)

## Task 1: Finalise baseline documentation across the repository

**Goal:** make the repository internally consistent and clearly reflect the current state of the project.

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
  - main transformer baselines completed with 5-run summaries
  - weighted RoBERTa as the current strongest overall model
  - weighted BERT as the stronger FAKE-recall comparison model
- remove outdated language such as:
  - 3-seed mean
  - single run
  - weighted BERT as the overall primary model
  - old sparse-baseline next-step language

**Reason:**
The experimental line has moved faster than the written project record.  
The repository now needs to present the current state clearly for both supervisor review and dissertation writing.

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
  - robustness / cross-dataset / generalisation discussion where relevant

**Minimum target for this period:**
- move beyond the earlier small paper set and build a more credible base for the dissertation

**Reason:**
The supervisor explicitly noted that the literature review was still too limited.  
Now that the model results are stronger and more stable, the literature review needs to catch up.

---

## Task 3: Write the current error analysis into thesis-ready form

**Goal:** convert the current model analysis into a form that can be used directly in the dissertation.

**Focus:**
- false positives
- false negatives
- remaining FAKE-class errors
- model trade-off between:
  - weighted BERT
  - weighted RoBERTa

**Outputs:**
- turn the existing error analysis into a more polished written subsection
- explain:
  - why FAKE recall remains difficult,
  - why weighted BERT catches more FAKE cases,
  - why weighted RoBERTa performs better overall,
  - why naive context concatenation and macro-F1 threshold tuning did not help

**Files to update:**
- `results/liar_baseline.md`
- optionally `notes/clean_notes.md`

**Reason:**
The project now has enough evidence to move beyond raw metric reporting.  
This is one of the most useful next steps for thesis writing.

---

# Week 2 (2026-04-23 to 2026-04-30)

## Task 4: Prepare the cross-dataset / cross-domain pipeline

**Goal:** begin the next stage of the project after the LIAR in-domain baseline line.

**Outputs:**
- define the next experimental pipeline beyond LIAR in-domain evaluation
- identify which dataset(s) will be used next
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

**Goal:** make the next supervisor update easy to review in advance.

**Outputs:**
- decide which files should be sent to the supervisor before the next meeting
- make sure those files are clean and fully up to date
- prioritise:
  - `results/baseline_results_summary.md`
  - `results/liar_baseline.md`
  - `progress/progress_summary.md`
  - `tracking.md`

**Reason:**
The supervisor asked to be told which files to review before the next meeting.

---

## Task 6: Keep further model work optional and limited

**Goal:** avoid spending too much time on small extra model variations unless they clearly add thesis value.

**Optional only if clearly justified:**
- one additional targeted experiment directly motivated by the current cross-dataset setup,
- or a model change that is strongly supported by the literature review.

**Reason:**
The current main bottleneck is no longer whether the project has a strong enough LIAR baseline.  
The bigger need now is:
- literature coverage,
- thesis-ready interpretation,
- and next-stage experiment design.

---

## Expected Deliverables by the End of This Period

By the end of this two-week period, the project should have:

1. a fully synchronised repository record of the current LIAR baselines,
2. a clearer and expanded literature review,
3. a thesis-ready written error analysis section,
4. an initial design for the cross-dataset / cross-domain stage,
5. a clean set of files ready to share with the supervisor.

---

## Notes on Scope

During this period, the main focus is **not** broad model tuning.

The main focus is to make the current results thesis-ready and to prepare the next research stage.

Further model experimentation should only continue if it clearly supports one of these goals:
- stronger interpretation,
- stronger comparison,
- or better preparation for the cross-dataset stage.
