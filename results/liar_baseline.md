# LIAR Baseline Results

> Purpose: record the LIAR in-domain binary baseline, including Version 1, Version 2 improvement, validation-based comparison, and current interpretation.

## 1) Run info (reproducibility)

* Latest update: 2026-03-31
* Code evidence:

  * `notebooks/01_liar_load_inspect_v2.ipynb`
  * `notebooks/02_tfidf_baseline_v2.ipynb`
* Output evidence:

  * `results/liar_baseline.md`
  * `results/liar_baseline_v2_run_output.md`
* Random seed: 42

---

## 2) Dataset

* Dataset: LIAR
* Files used:

  * `train.tsv`
  * `valid.tsv`
  * `test.tsv`
* Text field: `statement`
* Evaluation setting: **in-domain (LIAR → LIAR)**

Split sizes:

* Train: 10240
* Valid: 1284
* Test: 1267

### Binary mapping used in this project

* REAL (0): `true`, `mostly-true`, `half-true`
* FAKE (1): `barely-true`, `false`, `pants-fire`

### Label distribution after binary mapping

**Train**

* REAL: 5752
* FAKE: 4488

**Valid**

* REAL: 668
* FAKE: 616

**Test**

* REAL: 714
* FAKE: 553

---

## 3) Version 1 baseline

### Setup

* Model: TF-IDF + Logistic Regression
* Text preprocessing:

  * strip whitespace
  * remove empty statements
* Validation split:

  * not yet used for model selection in Version 1

### Version 1 result (test split)

* Accuracy: 0.6196
* Macro-F1: 0.5935

### Confusion matrix

Label order: `[REAL, FAKE]`

```text
[[553 161]
 [321 232]]
````

### Classification report

```text
              precision    recall  f1-score   support

        REAL     0.6330    0.7750    0.6960       714
        FAKE     0.5900    0.4200    0.4900       553

    accuracy                         0.6196      1267
   macro avg     0.6110    0.5980    0.5935      1267
weighted avg     0.6140    0.6196    0.6060      1267
```

---

## 4) Version 2 baseline improvement

### Goal

Version 2 was created to improve the LIAR binary baseline and to make model selection more systematic.

Main changes:

* use the fixed binary mapping for this project
* compare preprocessing settings on the validation split
* compare TF-IDF settings on the validation split
* use validation results for model selection
* evaluate the final selected configuration once on the test split

### Preprocessing comparison (validation)

Compared settings:

* `P0_minimal`
* `P1_lower`
* `P2_lower_stopwords`
* `P3_lower_stopwords_stemming`

Result summary:

* stronger preprocessing did **not** improve validation performance in the current LIAR binary setup
* `P0_minimal` and `P1_lower` produced the same validation score in this run
* stronger preprocessing with stopword removal and stemming performed worse

### TF-IDF comparison (validation)

Compared settings included:

* `(1,2), min_df=1, max_df=1.0`
* `(1,2), min_df=2, max_df=1.0`
* `(1,2), min_df=2, max_df=0.95`
* `(1,2), min_df=5, max_df=0.95`

### Selected Version 2 configuration

* Exp ID: `E6`
* Preprocess: `P0_minimal`
* `ngram_range=(1,2)`
* `min_df=2`
* `max_df=1.0`

### Why `min_df=2` and `max_df=1.0` are both valid

* `min_df=2` means a term is kept if it appears in at least two documents
* `max_df=1.0` means terms are not removed based on very high document frequency

So, although both values are numerical thresholds, they are not the same type of cutoff:

* `min_df` is a lower cutoff
* `max_df` is an upper cutoff

### Why E6 was selected instead of E5

The model selection rule in Version 2 prioritised **Macro-F1** on the validation split, with Accuracy used as a secondary criterion.

* `E5` had the highest validation Accuracy (`0.6254`)
* `E6` had the highest validation Macro-F1 (`0.6123`)
* `E7` matched `E6` on both validation Accuracy and Macro-F1

Because Macro-F1 was treated as the primary selection metric, **E6** was retained as the final Version 2 configuration.

---

## 5) Version 2 result (test split)

### Main metrics

* Accuracy: **0.6235**
* Macro-F1: **0.6005**

### Difference vs Version 1

* Accuracy delta: **+0.0039**
* Macro-F1 delta: **+0.0070**

### Confusion matrix

Label order: `[REAL, FAKE]`

```text
[[547 167]
 [310 243]]
```

### Classification report

```text
              precision    recall  f1-score   support

        REAL     0.6383    0.7661    0.6964       714
        FAKE     0.5927    0.4394    0.5047       553

    accuracy                         0.6235      1267
   macro avg     0.6155    0.6028    0.6005      1267
weighted avg     0.6184    0.6235    0.6127      1267
```

---

## 6) Validation experiments summary

### 6.1 Preprocessing comparison (validation)

| Exp ID | Preprocess                  | Lowercase | Stopword Removal | Stemming | ngram_range | min_df | max_df | Accuracy | Macro-F1 | n_features |
| ------ | --------------------------- | --------- | ---------------- | -------- | ----------- | -----: | -----: | -------: | -------: | ---------: |
| E1     | P0_minimal                  | No        | No               | No       | (1,1)       |      1 |    1.0 |   0.6090 |   0.5993 |      12196 |
| E2     | P1_lower                    | Yes       | No               | No       | (1,1)       |      1 |    1.0 |   0.6090 |   0.5993 |      12196 |
| E4     | P3_lower_stopwords_stemming | Yes       | Yes              | Yes      | (1,1)       |      1 |    1.0 |   0.5974 |   0.5876 |       7625 |
| E3     | P2_lower_stopwords          | Yes       | Yes              | No       | (1,1)       |      1 |    1.0 |   0.5974 |   0.5874 |      11342 |

**Observation.** In the current LIAR binary setup, stronger preprocessing did not improve validation performance. `P0_minimal` and `P1_lower` produced identical validation scores in this run, while the stronger preprocessing settings performed worse.

---

### 6.2 TF-IDF comparison (validation)

| Exp ID | Preprocess | ngram_range | min_df | max_df | Accuracy | Macro-F1 | n_features |
| ------ | ---------- | ----------- | -----: | -----: | -------: | -------: | ---------: |
| E6     | P0_minimal | (1,2)       |      2 |   1.00 |   0.6231 |   0.6123 |      25788 |
| E7     | P0_minimal | (1,2)       |      2 |   0.95 |   0.6231 |   0.6123 |      25788 |
| E8     | P0_minimal | (1,2)       |      5 |   0.95 |   0.6199 |   0.6118 |       8212 |
| E5     | P0_minimal | (1,2)       |      1 |   1.00 |   0.6254 |   0.6112 |      95883 |

**Observation.** Under the best preprocessing setting (`P0_minimal`), the strongest validation Macro-F1 was achieved by **E6** and **E7**. Although **E5** had the highest validation Accuracy, it had a slightly lower Macro-F1. Since Version 2 used Macro-F1 as the primary model selection metric, **E6** was selected.

---

### 6.3 Selected best validation configuration

* Exp ID: `E6`
* Preprocessing: `P0_minimal`
* `ngram_range=(1,2)`
* `min_df=2`
* `max_df=1.0`
* Validation Accuracy: `0.6231`
* Validation Macro-F1: `0.6123`

This configuration was selected using the validation split and then evaluated once on the test split.

---

## 7) Literature comparison (short)

The supervisor asked for a comparison with previous LIAR results.

* The original LIAR paper introduced the dataset as a **6-class benchmark** with about **12.8K short political statements**, and evaluated several text-based baselines on that harder fine-grained setting. This is useful background, but it is **not directly comparable** to the current binary setup. ([aclanthology.org][1])
* A more recent paper, **TELLER (2024)**, reports in-domain **binary classification** results on LIAR of:

  * BERT: Accuracy `63.06`, Macro-F1 `62.42`
  * RoBERTa: Accuracy `64.55`, Macro-F1 `63.16`
  * TELLER (best): Accuracy `67.73`, Macro-F1 `66.97`

### Current position relative to the literature

The current project result:

* Accuracy: `0.6235`
* Macro-F1: `0.6005`

This suggests that:

* the current LIAR binary baseline is in the general range of a **simple traditional baseline**
* but it is still below stronger modern baselines reported in the literature
* further improvement is still needed before moving confidently to stronger models

---

## 8) Current interpretation

### What Version 2 shows

* Version 2 is more systematic than Version 1 because it uses the validation split for model selection before final testing.
* Compared with Version 1, Version 2 improves slightly on both Accuracy and Macro-F1.

### Main observations from validation

* `P0_minimal` and `P1_lower` gave identical validation results in this run.
* Stronger preprocessing with stopword removal and stemming performed worse.
* In the TF-IDF comparison, **E6** and **E7** gave the best validation Macro-F1, while **E5** gave the highest validation Accuracy but a slightly lower Macro-F1.

### Main remaining weakness

* The model still performs better on the **REAL** class than on the **FAKE** class.
* FAKE recall remains relatively low (`0.4394`), which continues to limit Macro-F1.

### Likely explanation

* LIAR is a difficult dataset of short political claims.
* Some stronger preprocessing steps may remove or distort useful lexical cues in short statements.
* The remaining limitation may be more related to feature representation and classifier behaviour than to simple text cleaning alone.

---

## 9) Next steps

* compare Logistic Regression with `class_weight="balanced"`
* compare Logistic Regression with `LinearSVC`
* keep the traditional baseline improvement stage active before moving to stronger models
* retain this file as the main place for:

  * Version 1 vs Version 2 comparison
  * validation experiment summary
  * literature comparison
  * interpretation of remaining error patterns

