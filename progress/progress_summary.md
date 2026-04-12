# Progress Summary (living document)

> Note (for supervisor): the up-to-date task tracker is maintained in `tracking.md` as the single source of truth.  
> This file provides short narrative context only.

## Latest update: 2026-04-12 (Ireland time)

## What I did this week

This week I focused on making the current transformer results more reliable and on testing the most direct follow-up ideas, rather than continuing broad model changes.

### 1. Extended the unweighted BERT stability check
- I extended the unweighted BERT baseline from **3 runs to 5 runs**.
- The new 5-run mean is:
  - **Test Accuracy:** `0.6425 ± 0.0095`
  - **Test Macro-F1:** `0.6231 ± 0.0122`

Main point:
- the BERT improvement over TF-IDF still holds,
- but seed variance is real,
- so reporting mean and standard deviation is more appropriate than relying on a single run.

### 2. Completed a more concrete error analysis
- I completed an error analysis comparing representative **weighted BERT** and **weighted RoBERTa** checkpoints.
- The analysis now identifies concrete recurring error types rather than only reporting class-wise metrics.

Main patterns:
- `numeric_claim`
- `label_boundary_ambiguity`
- `context_dependent`

Main interpretation:
- weighted BERT is more willing to predict **FAKE**, so it achieves stronger FAKE recall,
- weighted RoBERTa appears more conservative and better calibrated overall.

### 3. Tested statement-only vs statement + context
- I ran a controlled comparison using the weighted RoBERTa setup, changing only the input text:
  - `statement_only`
  - `statement + [CTX] + context`

Main result:
- naive context concatenation did **not** improve performance.
- It reduced:
  - test accuracy
  - test macro-F1
  - FAKE recall

Main interpretation:
- in LIAR, the `context` field often behaves more like source or venue metadata than true factual background,
- so directly concatenating it adds noise rather than useful evidence.

### 4. Tested threshold tuning for weighted RoBERTa
- I scanned decision thresholds on the validation set while keeping the same trained weighted RoBERTa model.
- The validation macro-F1 optimum shifted to a more conservative threshold.

Main result:
- threshold tuning based on validation **macro-F1** did **not** improve test performance.
- It reduced FAKE recall on the test set.

Main interpretation:
- simply tuning the threshold for macro-F1 does not automatically solve the conservative FAKE boundary problem,
- and lower-threshold operating points may only be useful if the objective changes from macro-F1 to FAKE recall.

---

## Main findings this week

- The unweighted BERT baseline is more stable when averaged over 5 runs than when reported from only 3 runs.
- The current remaining difficulty is still concentrated in:
  - numeric claims,
  - narrow label boundaries,
  - and missing context.
- Naive context concatenation is **not** a useful next step for the current LIAR setup.
- Macro-F1-based threshold tuning is also **not** a good direct fix for the current FAKE recall weakness.
- This means the model line is now better understood, and the most obvious low-cost follow-up ideas have already been tested.

---

## Main current issue

The current issue is no longer basic modelling setup.

The main issue is now how to interpret the remaining performance gap and decide whether additional model work is still worthwhile.

At this stage:
- the gains from stronger models are real but moderate,
- the task itself remains difficult because of label ambiguity and context dependence,
- and further small model variations may have lower value than analysis, literature, and next-stage experiment design.

---

## Next step for next week

The next priorities should now be:

1. expand the literature review,
2. write the current error analysis into a thesis-ready subsection,
3. finalise the current model comparison more clearly in the repo files,
4. begin planning the cross-dataset / cross-domain stage.

Additional model work should now be treated as optional unless it clearly supports one of those goals.

---

## Project status to date (short)

The project has now moved beyond the traditional sparse-baseline stage.

### Dataset and task
- Dataset: **LIAR**
- Setting: **in-domain binary classification**
- Input text: `statement`
- Binary mapping:
  - REAL (0): `true`, `mostly-true`, `half-true`
  - FAKE (1): `barely-true`, `false`, `pants-fire`

Split sizes:
- Train: 10240
- Valid: 1284
- Test: 1267

### Baselines completed so far

#### 1. TF-IDF + Logistic Regression
- Final sparse baseline:
  - **Accuracy:** `0.6235`
  - **Macro-F1:** `0.6005`

Main observation:
- better performance on **REAL** than on **FAKE**
- limited FAKE recall

#### 2. Unweighted BERT
- 5-run mean:
  - **Accuracy:** `0.6425 ± 0.0095`
  - **Macro-F1:** `0.6231 ± 0.0122`

Main observation:
- stable improvement over TF-IDF
- but FAKE recall remains weaker than REAL recall

#### 3. Weighted BERT
- 3-run mean:
  - **Accuracy:** `0.6404 ± 0.0078`
  - **Macro-F1:** `0.6304 ± 0.0081`
  - **REAL recall:** `0.7129 ± 0.0194`
  - **FAKE recall:** `0.5467 ± 0.0241`

Main observation:
- weighted loss improves macro-F1
- weighted loss improves FAKE recall
- weighted BERT remains an important class-balanced model

#### 4. RoBERTa line
- RoBERTa baselines and follow-up checks have now been run as comparison models.
- The recent follow-up analyses suggest:
  - stronger overall calibrated performance in some settings,
  - but not necessarily the strongest FAKE recall.

This part is now better understood through error analysis and targeted follow-up tests, rather than only raw score comparison.

---

## Main remaining gaps

### 1. Literature review is still too limited
The experimental line is now ahead of the reading and writing line.

What this means:
- more paper summaries are still needed,
- and the current results need to be positioned more clearly against prior work.

### 2. Cross-dataset / cross-domain work has not properly started yet
The LIAR in-domain baseline line is now strong enough to support the next stage, but the cross-dataset pipeline is still missing.

### 3. Analysis now needs to be turned into thesis writing
The project now has enough material for:
- a stronger Results section,
- a clearer Discussion section,
- and a proper Error Analysis subsection.

---

## Current risk

The main current risk is spending too much time on extra model variations that may only produce small gains.

At this stage, the more valuable work is likely to be:
- literature review,
- interpretation,
- and cross-dataset planning,
rather than further incremental model tuning.

Dates and detailed task status are tracked in:

`tracking.md`
