# LIAR Baseline Results Summary

## Task
This file summarises the current **in-domain binary fake news detection baselines** on the **LIAR** dataset.

The project uses the following binary label mapping:

- **REAL (0):** `true`, `mostly-true`, `half-true`
- **FAKE (1):** `barely-true`, `false`, `pants-fire`

All current baseline experiments use **statement** as the main input text unless explicitly stated otherwise.

## Dataset
Split sizes:

- **Train:** 10240
- **Valid:** 1284
- **Test:** 1267

## Baseline development path
The baseline line has progressed through the following stages:

1. **TF-IDF + Logistic Regression**
2. **BERT-base**
3. **BERT-base + weighted loss**
4. **RoBERTa-base + weighted loss**
5. targeted follow-up checks based on error analysis

## Main results

| Model | Accuracy | Macro-F1 | Notes |
|---|---:|---:|---|
| TF-IDF + Logistic Regression | 0.6235 | 0.6005 | Final sparse baseline; effectively deterministic |
| BERT-base (5-run mean) | 0.6425 ± 0.0095 | 0.6231 ± 0.0122 | Mean over seeds 42, 52, 62, 72, 82 |
| BERT-base + weighted loss (5-run mean) | 0.6412 ± 0.0065 | 0.6322 ± 0.0090 | Mean over 5 runs; stronger FAKE recall |
| RoBERTa-base + weighted loss (5-run mean) | 0.6522 ± 0.0074 | 0.6396 ± 0.0080 | Mean over 5 runs; current strongest overall model |

## Class-wise recall summary

| Model | REAL Recall | FAKE Recall | Notes |
|---|---:|---:|---|
| TF-IDF + Logistic Regression | 0.7661 | 0.4394 | Sparse baseline |
| BERT-base (5-run mean) | N/A | N/A | Not available in the saved 5-run result file |
| BERT-base + weighted loss (5-run mean) | 0.7048 ± 0.0292 | 0.5591 ± 0.0447 | Best FAKE recall among current baselines |
| RoBERTa-base + weighted loss (5-run mean) | 0.7443 ± 0.0153 | 0.5335 ± 0.0199 | Stronger overall balance, but lower FAKE recall than weighted BERT |

## Current model status
At the current stage, the LIAR baseline line is now strong enough for this phase of the project.

The main comparison is no longer just between sparse and neural baselines.  
It is now mainly about the trade-off between:

- **weighted BERT**, which is stronger on **FAKE recall**
- **weighted RoBERTa**, which is stronger on **overall performance**

## Current main interpretation
The current results suggest four main conclusions.

### 1. Transformer baselines consistently outperform the sparse baseline
The project has now clearly moved beyond the traditional TF-IDF-only stage.

Compared with TF-IDF + Logistic Regression, transformer baselines produce higher overall accuracy and higher macro-F1 on the LIAR binary task.

### 2. The gain from TF-IDF to transformers is meaningful but moderate
The improvement is real and stable, but not dramatic.

This is consistent with the difficulty of the LIAR dataset:
- the statements are short,
- the label boundary becomes narrow after binary compression,
- and many claims remain difficult even for stronger transformer models.

### 3. Class balance remains a central challenge
Across the baselines, one of the most important recurring issues is the imbalance between performance on **REAL** and **FAKE**.

This is one reason why simple overall accuracy is not enough to judge model quality in this project.

### 4. Weighted training is useful, but different weighted models optimise different strengths
The current weighted transformer results suggest a clear division:

- **weighted BERT** is more willing to predict **FAKE**, so it remains important when the priority is stronger FAKE recall,
- **weighted RoBERTa** is more conservative and better calibrated overall, so it is currently stronger when the priority is overall performance.

## TF-IDF note
The TF-IDF + Logistic Regression baseline was checked across 5 seeds.

All 5 runs were identical, which shows that the current sparse pipeline is effectively deterministic in this setup.  
Repeated seed runs are therefore **not** a meaningful stability experiment for this baseline.

## Error-analysis-guided follow-up checks
Two direct follow-up ideas were tested after the main model line had been established.

### 1. Statement-only vs statement + context
A controlled weighted RoBERTa comparison tested:

- `statement_only`
- `statement + " [CTX] " + context`

Result:
- direct context concatenation **did not improve** performance,
- it reduced test accuracy,
- it reduced test macro-F1,
- and it reduced FAKE recall.

Interpretation:
- the LIAR `context` field often behaves more like source or venue metadata than true factual background,
- so naive concatenation adds noise rather than useful evidence.

### 2. Threshold tuning for weighted RoBERTa
Validation-set threshold tuning was also tested.

Result:
- selecting the threshold by validation macro-F1 did **not** improve the test result,
- and it further reduced FAKE recall.

Interpretation:
- the current conservative FAKE boundary is not solved by simple threshold tuning under a macro-F1 objective,
- so threshold tuning is not a strong next-step direction under the current evaluation priority.

## Current conclusion
The current baseline line is now mature enough for the present project stage.

The strongest overall summary is:

- **TF-IDF + Logistic Regression** remains the main sparse baseline,
- **BERT-base** is the main unweighted neural baseline,
- **weighted BERT** remains important because of its stronger FAKE recall,
- **weighted RoBERTa** is currently the strongest overall model.

For thesis writing, the most defensible interpretation is:

- **weighted RoBERTa** should be treated as the current main overall model,
- while **weighted BERT** should be retained as the key comparison model for class-balance and FAKE-recall analysis.

## Next priorities
The next project priorities are no longer broad model exploration.

The main next steps are now:

1. expand the literature review,
2. turn the current error analysis into a thesis-ready subsection,
3. prepare the cross-dataset / cross-domain pipeline,
4. keep any further model work limited to clearly justified cases only.

## Notes
- This file should remain a short high-level summary.
- Detailed per-run results should stay in the dedicated result files.
- The detailed LIAR baseline record should remain in `results/liar_baseline.md`.
