# LIAR Baseline Results

> Purpose: record the current LIAR in-domain binary baseline results, including the sparse baseline, transformer baselines, stability checks, direct comparisons, and error-analysis-guided interpretation.

## 1) Task setup

- Dataset: **LIAR**
- Evaluation setting: **in-domain (LIAR → LIAR)**
- Main input text: **statement**
- Files used:
  - `train.tsv`
  - `valid.tsv`
  - `test.tsv`

### Binary mapping used in this project

- **REAL (0):** `true`, `mostly-true`, `half-true`
- **FAKE (1):** `barely-true`, `false`, `pants-fire`

### Split sizes

- Train: 10240
- Valid: 1284
- Test: 1267

### Label distribution after binary mapping

**Train**
- REAL: 5752
- FAKE: 4488

**Valid**
- REAL: 668
- FAKE: 616

**Test**
- REAL: 714
- FAKE: 553

---

## 2) Main results overview

| Model | Accuracy | Macro-F1 | REAL Recall | FAKE Recall | Notes |
|---|---:|---:|---:|---:|---|
| TF-IDF + Logistic Regression | 0.6235 | 0.6005 | 0.7661 | 0.4394 | Final sparse baseline; effectively deterministic |
| BERT-base (5-run mean) | 0.6425 ± 0.0095 | 0.6231 ± 0.0122 | N/A | N/A | Main unweighted neural baseline |
| BERT-base + weighted loss (5-run mean) | 0.6412 ± 0.0065 | 0.6322 ± 0.0090 | 0.7048 ± 0.0292 | 0.5591 ± 0.0447 | Stronger FAKE recall |
| RoBERTa-base + weighted loss (5-run mean) | 0.6522 ± 0.0074 | 0.6396 ± 0.0080 | 0.7443 ± 0.0153 | 0.5335 ± 0.0199 | Current strongest overall model |

---

## 3) Sparse baseline: TF-IDF + Logistic Regression

### Final result
- Accuracy: `0.6235`
- Macro-F1: `0.6005`

### Confusion matrix
Label order: `[REAL, FAKE]`

```text
[[547 167]
 [310 243]]
````

### Classification report

```text
              precision    recall  f1-score   support

        REAL     0.6383    0.7661    0.6964       714
        FAKE     0.5927    0.4394    0.5047       553

    accuracy                         0.6235      1267
   macro avg     0.6155    0.6028    0.6005      1267
weighted avg     0.6184    0.6235    0.6127      1267
```

### Interpretation

The sparse baseline performs better on the **REAL** class than on the **FAKE** class, and its main limitation is the relatively weak **FAKE recall**.

A 5-seed determinism check showed that the current TF-IDF pipeline is effectively deterministic in this setup, so repeated seed runs are not a meaningful stability experiment for this baseline.

---

## 4) Unweighted BERT baseline

The unweighted BERT baseline was extended to **5 runs**.

### 5-run mean and standard deviation

* Test accuracy: `0.6425 ± 0.0095`
* Test macro-F1: `0.6231 ± 0.0122`

### Interpretation

Compared with the TF-IDF baseline, unweighted BERT consistently improves both accuracy and macro-F1.

The gain is real, but still moderate rather than dramatic. This suggests that LIAR remains a difficult dataset even for stronger transformer models.

---

## 5) Weighted BERT baseline

To address the class-balance weakness of the unweighted BERT baseline, class-weighted loss was applied using weights computed from the **train split only**.

### 5-run mean and standard deviation

* Test accuracy: `0.6412 ± 0.0065`
* Test macro-F1: `0.6322 ± 0.0090`
* REAL recall: `0.7048 ± 0.0292`
* FAKE recall: `0.5591 ± 0.0447`

### Interpretation

Weighted BERT improves macro-F1 relative to the unweighted BERT baseline and gives stronger **FAKE recall**.

Its main value is not that it becomes the strongest model overall, but that it shifts the decision boundary toward catching more FAKE examples.

This makes it a particularly useful comparison model for analysing class balance and FAKE-recall behaviour.

---

## 6) Weighted RoBERTa baseline

RoBERTa was also extended to a weighted-loss setup under the same LIAR binary configuration.

### 5-run mean and standard deviation

* Test accuracy: `0.6522 ± 0.0074`
* Test macro-F1: `0.6396 ± 0.0080`
* REAL recall: `0.7443 ± 0.0153`
* FAKE recall: `0.5335 ± 0.0199`

### Interpretation

Weighted RoBERTa is currently the **strongest overall model**.

It gives the highest mean accuracy and the highest mean macro-F1 among the tested baselines.

However, compared with weighted BERT, it is slightly more conservative on the FAKE class and therefore gives lower FAKE recall.

---

## 7) Direct comparison of the current main baselines

### Unweighted BERT vs TF-IDF

* Accuracy delta: `+0.0190`
* Macro-F1 delta: `+0.0226`

### Weighted BERT vs unweighted BERT

* Accuracy delta: `-0.0013`
* Macro-F1 delta: `+0.0091`

### Weighted RoBERTa vs weighted BERT

* Accuracy delta: `+0.0110`
* Macro-F1 delta: `+0.0074`
* REAL recall delta: `+0.0395`
* FAKE recall delta: `-0.0256`

### Comparison interpretation

These comparisons show the current trade-off clearly:

* **weighted RoBERTa** is stronger on **overall performance**
* **weighted BERT** is stronger on **FAKE recall**

This means the project no longer has a single “best in every sense” model.
Instead, the current model line reveals a meaningful trade-off between overall calibration and FAKE sensitivity.

---

## 8) Error analysis summary

A more detailed error analysis was carried out by comparing representative **weighted BERT** and **weighted RoBERTa** checkpoints.

### Main recurring error types

The most common remaining error patterns are:

* `numeric_claim`
* `label_boundary_ambiguity`
* `context_dependent`

### Why FAKE recall remains difficult

Three factors make the FAKE class difficult:

1. **Narrow label boundary**
   The binary mapping compresses the original 6-way labels into two classes, which makes the boundary between REAL and FAKE semantically narrow.

2. **Numeric claims**
   Many difficult examples involve numbers, rankings, or factual comparisons that are hard to verify from surface text alone.

3. **Missing context**
   Many LIAR statements are short and politically context-dependent, so the `statement` alone often lacks enough information.

### Weighted BERT vs weighted RoBERTa

The error analysis suggests the following trade-off:

* **weighted BERT** is more willing to predict **FAKE**
* **weighted RoBERTa** is more conservative and better calibrated overall

This explains why:

* weighted BERT gives stronger FAKE recall
* weighted RoBERTa gives stronger overall accuracy and macro-F1

---

## 9) Error-analysis-guided follow-up checks

Two direct follow-up ideas were tested after the main model line had been established.

### 1. Statement-only vs statement + context

A controlled weighted RoBERTa comparison tested:

* `statement_only`
* `statement + " [CTX] " + context`

#### Result

Direct context concatenation did **not** improve performance.

It reduced:

* test accuracy
* test macro-F1
* FAKE recall

#### Interpretation

In LIAR, the `context` field often behaves more like source or venue metadata than true factual background.
As a result, naive concatenation adds noise rather than useful evidence.

---

### 2. Threshold tuning for weighted RoBERTa

Validation-set threshold tuning was also tested.

#### Result

Selecting the threshold by validation macro-F1 did **not** improve the test result.

It also reduced FAKE recall.

#### Interpretation

The current conservative FAKE boundary is not solved by simple threshold tuning under a macro-F1 objective.

This means threshold tuning is not a strong direct improvement path under the current evaluation priority.

---

## 10) Literature comparison (short)

The original LIAR paper introduced the dataset as a 6-class benchmark of short political statements. That paper is useful as dataset background, but its results are not directly comparable to the current binary setup.

More recent transformer-based fake news detection work suggests that the current project is operating in the correct model family, but still below more advanced systems reported in the literature.

The current project position is therefore:

* clearly stronger than the sparse baseline,
* clearly improved by transformer fine-tuning,
* further improved by weighted training,
* but still constrained by task difficulty, label ambiguity, and context dependence.

---

## 11) Main interpretation

The current LIAR baseline line suggests four main conclusions.

### 1. Transformer baselines consistently outperform the sparse baseline

The project has clearly moved beyond the TF-IDF-only stage.

### 2. The gain from TF-IDF to transformers is meaningful but moderate

The improvement is real and stable, but not dramatic, which is consistent with the difficulty of LIAR.

### 3. Class balance remains a central challenge

Across models, one of the main remaining issues is the imbalance between performance on **REAL** and **FAKE**.

### 4. Weighted training is useful, but different weighted models optimise different strengths

* **weighted BERT** is stronger on FAKE recall
* **weighted RoBERTa** is stronger on overall performance

---

## 12) Current conclusion

At the current stage of the project:

* **TF-IDF + Logistic Regression** is the main sparse baseline,
* **BERT-base** is the main unweighted neural baseline,
* **weighted BERT** is the key comparison model for FAKE-recall and class-balance analysis,
* **weighted RoBERTa** is the current strongest overall model.

The strongest overall conclusion is therefore:

* **weighted RoBERTa** should be treated as the current main overall model,
* while **weighted BERT** should be retained as the most useful comparison model for understanding FAKE recall and decision-boundary trade-offs.
