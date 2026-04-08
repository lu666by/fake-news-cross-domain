# Progress Summary (living document)

> Note (for supervisor): the up-to-date task tracker is maintained in `tracking.md` as the single source of truth.  
> This file provides short narrative context only.

## Latest update: 2026-04-08 (Ireland time)

## What I have achieved

Since the previous update, I have moved the project beyond the traditional sparse baseline stage and completed the first strong transformer baselines for the LIAR binary task.

### 1. Repository organisation and tracking
- `tracking.md` remains the main place for task status and evidence links.
- `plans/` and `progress/` files remain short and are used only for narrative context.
- The baseline results have now been reorganised into clearer result summaries.

### 2. LIAR dataset loading and inspection
- `notebooks/01_liar_load.ipynb` loads the LIAR `train`, `valid`, and `test` splits.
- The notebook inspects:
  - dataset shapes
  - binary label distribution
  - example statements
  - example contexts
  - simple text statistics

Current LIAR split sizes:
- Train: 10240
- Valid: 1284
- Test: 1267

Binary mapping used in this project:
- REAL (0): `true`, `mostly-true`, `half-true`
- FAKE (1): `barely-true`, `false`, `pants-fire`

### 3. Traditional sparse baseline completed
The TF-IDF + Logistic Regression baseline has now been completed and documented as the main traditional baseline.

Final sparse baseline result:
- Accuracy: 0.6235
- Macro-F1: 0.6005

Main observation:
- the sparse baseline performs better on the REAL class than on the FAKE class
- FAKE recall remains limited

### 4. Unweighted BERT baseline completed
A BERT-base baseline was implemented and run successfully on GPU.

Main result:
- single run:
  - Accuracy: 0.6401
  - Macro-F1: 0.6231
- 3-seed mean:
  - Accuracy: 0.6369 ± 0.0028
  - Macro-F1: 0.6169 ± 0.0054

Main observation:
- BERT consistently improves over TF-IDF
- the improvement is stable across seeds
- however, FAKE recall is still weaker than REAL recall

### 5. Weighted BERT baseline completed
A separate weighted-loss BERT experiment was created and evaluated across 3 random seeds.

Weighted BERT 3-seed mean:
- Accuracy: 0.6404 ± 0.0078
- Macro-F1: 0.6304 ± 0.0081
- REAL recall: 0.7129 ± 0.0194
- FAKE recall: 0.5467 ± 0.0241

Main observation:
- weighted loss improves macro-F1 compared with unweighted BERT
- weighted loss improves FAKE recall
- weighted BERT currently gives the best class-balanced result among the tested baselines

### 6. RoBERTa baseline completed
A separate RoBERTa baseline was also run successfully.

RoBERTa single-run result:
- Accuracy: 0.6504
- Macro-F1: 0.6262

Main observation:
- RoBERTa gives the highest current single-run accuracy
- however, it does not outperform weighted BERT on Macro-F1
- it is currently treated as an important comparison model rather than the primary model

---

## Key takeaways so far

- The project has now moved beyond the traditional baseline-only stage.
- Transformer baselines consistently outperform the TF-IDF baseline on LIAR binary classification.
- The improvement from TF-IDF to BERT is stable but moderate rather than dramatic.
- Class balance remains a central issue in the task.
- Weighted loss is an effective and interpretable improvement because it improves FAKE recall and produces the strongest overall Macro-F1.
- At the current stage, **weighted BERT** is the most suitable primary model.

---

## Current model status

### Completed
- LIAR dataset loading and inspection
- TF-IDF baseline
- BERT baseline
- BERT 3-seed stability check
- weighted BERT baseline
- weighted BERT 3-seed stability check
- RoBERTa baseline

### Current main model
- **Primary model:** weighted BERT
- Reason:
  - best mean Macro-F1 among tested baselines
  - better balance between REAL and FAKE
  - more suitable than RoBERTa if balanced performance is prioritised over raw accuracy

---

## Main remaining gaps

### 1. Literature review is still too limited
The supervisor previously noted that the literature review was not yet sufficient.

What this means:
- the project now has stronger experimental progress than before
- but the related-work section still needs to be expanded
- more paper summaries and clearer positioning against prior work are still needed

Why it matters:
- the dissertation needs stronger literature coverage
- the experimental results now need to be framed more clearly against existing work

### 2. Cross-dataset / cross-domain work has not started properly yet
The supervisor previously indicated that stronger models should be established first, and then the cross part should follow.

What this means:
- the LIAR in-domain baseline line is now much stronger
- but the cross-dataset pipeline is still not in place

Why it matters:
- this is likely to become one of the next major parts of the dissertation
- model-only improvement is no longer the main bottleneck

### 3. Error analysis still needs to be written up
The project now has enough model evidence to support more detailed analysis, but the error analysis section is still missing.

What this means:
- I can now analyse false positives, false negatives, and remaining FAKE-class errors
- this would strengthen the Results and Discussion sections

Why it matters:
- the dissertation needs interpretation, not only performance numbers
- weighted BERT is especially suitable for this analysis because it changes class balance in an interpretable way

---

## Current risks

### Risk 1: spending too much time on small extra model variations
Now that weighted BERT is already a strong main baseline, further minor tuning may give only small gains.

Why this matters:
- time is probably better spent on literature review, analysis, and cross-dataset work

### Risk 2: experimental line is ahead of the writing line
The modelling progress is now much stronger than the documentation and literature review progress.

Why this matters:
- this can create a gap between what has been implemented and what is ready to be written into the dissertation

---

## Next actions

The next project priorities are now:

1. write up the current baseline results more cleanly across the project files
2. expand the literature review and add more paper summaries
3. carry out error analysis for the weighted BERT model
4. design and begin the cross-dataset / cross-domain pipeline
5. keep additional model work optional rather than central

Optional extra experiment only if time allows:
- RoBERTa + weighted loss
- statement vs statement + context comparison

Dates and detailed task status are tracked in:

`tracking.md`
