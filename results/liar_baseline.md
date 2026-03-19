
---

# LIAR Baseline Results

> Purpose: record the LIAR in-domain binary baseline, including Version 1, Version 2 improvement, validation-based comparison, and current interpretation.

## 1) Run info (reproducibility)

* Latest update: 2026-03-19
* Code evidence:

  * `notebooks/01_liar_load.ipynb`
  * `notebooks/02_tfidf_baseline.ipynb`
* Output evidence:

  * `results/liar_overview.md`
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
```

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
* compare preprocessing settings
* compare TF-IDF settings on the validation split
* evaluate the final selected configuration once on the test split

### Preprocessing comparison (validation)

Compared settings:

* `P0_minimal`
* `P1_lower`
* `P2_lower_stopwords`
* `P3_lower_stopwords_stemming`

Result summary:

* stronger preprocessing did **not** improve validation performance in the current LIAR binary setup
* the best validation result in Phase 1 came from `P0_minimal`

### TF-IDF comparison (validation)

Compared settings included:

* `(1,2), min_df=1, max_df=1.0`
* `(1,2), min_df=2, max_df=1.0`
* `(1,2), min_df=2, max_df=0.95`
* `(1,2), min_df=5, max_df=0.95`

### Selected Version 2 configuration

* Preprocess: `P0_minimal`
* `ngram_range=(1,2)`
* `min_df=1`
* `max_df=1.0`

### Why `min_df=1` and `max_df=1.0` are both valid

* `min_df=1` means a term is kept if it appears in at least one document
* `max_df=1.0` means terms are not removed based on very high document frequency

So, although both values look like “1”, they are not the same type of threshold:

* `min_df` is a lower cutoff
* `max_df` is an upper cutoff

This relatively simple setting was kept because it gave the best validation result in the current comparison.

---

## 5) Version 2 result (test split)

### Main metrics

* Accuracy: 0.6243
* Macro-F1: 0.5968

### Difference vs Version 1

* Accuracy delta: +0.0047
* Macro-F1 delta: +0.0033

### Confusion matrix

Label order: `[REAL, FAKE]`

```text
[[561 153]
 [323 230]]
```

### Classification report

```text
              precision    recall  f1-score   support

        REAL     0.6346    0.7857    0.7021       714
        FAKE     0.6005    0.4159    0.4915       553

    accuracy                         0.6243      1267
   macro avg     0.6176    0.6008    0.5968      1267
weighted avg     0.6197    0.6243    0.6102      1267
```

---

## 6) Validation experiments summary

| Exp ID | Phase      | Preprocess                  | ngram_range | min_df | max_df | Accuracy | Macro-F1 |
| ------ | ---------- | --------------------------- | ----------- | -----: | -----: | -------: | -------: |
| E5     | tfidf      | P0_minimal                  | (1,2)       |      1 |    1.0 |   0.6301 |   0.6149 |
| E6     | tfidf      | P0_minimal                  | (1,2)       |      2 |    1.0 |   0.6215 |   0.6113 |
| E7     | tfidf      | P0_minimal                  | (1,2)       |      2 |   0.95 |   0.6215 |   0.6113 |
| E8     | tfidf      | P0_minimal                  | (1,2)       |      5 |   0.95 |   0.6160 |   0.6066 |
| E1     | preprocess | P0_minimal                  | (1,1)       |      1 |    1.0 |   0.6114 |   0.6018 |
| E2     | preprocess | P1_lower                    | (1,1)       |      1 |    1.0 |   0.6090 |   0.5993 |
| E4     | preprocess | P3_lower_stopwords_stemming | (1,1)       |      1 |    1.0 |   0.5974 |   0.5876 |
| E3     | preprocess | P2_lower_stopwords          | (1,1)       |      1 |    1.0 |   0.5974 |   0.5874 |

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

* Accuracy: 0.6243
* Macro-F1: 0.5968

This suggests that:

* the current LIAR binary baseline is in the general range of a **simple traditional baseline**
* but it is still below stronger modern baselines reported in the literature
* further improvement is still needed before moving confidently to stronger models

---

## 8) Current interpretation

### What Version 2 shows

* Version 2 is more systematic than Version 1 because it uses validation-based comparison before final testing.
* However, the improvement over Version 1 is still small.

### Main remaining weakness

* The model still performs noticeably better on the REAL class than on the FAKE class.
* FAKE recall remains low, which keeps Macro-F1 relatively low.

### Likely explanation

* LIAR is a difficult dataset of short political claims.
* In the current setup, stronger preprocessing did not help.
* The main remaining issue may be class handling and classifier choice, rather than simple text cleaning alone.

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

---

