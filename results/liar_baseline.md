# LIAR Baseline Results

> Purpose: record the first reproducible baseline on LIAR (in-domain), with clear setup and metrics.

## 1) Run info (reproducibility)

- Date: 2026-03-12
- Code evidence:
  - Notebook: `notebooks/02_tfidf_baseline.ipynb`
  - (Optional) Commit/PR link:
- Environment:
  - Python: not recorded
  - sklearn: not recorded
- Random seed (if used): 42

---

## 2) Dataset

- Dataset: LIAR (train/valid/test TSV)
- Text field: `statement`
- Split used for reporting: **test.tsv**

Basic counts:

- Train: 10240
- Valid: 1284
- Test: 1267

Label setting used in this run:

- ☐ 6-class (original LIAR labels)
- ☑ Binary (REAL/FAKE mapping; specified below)

---

## 3) Preprocessing

Text cleaning:

- ☑ strip whitespace
- ☒ lowercasing: no explicit lowercasing step

Filtering:

- removed empty statements

Notes:

- only the `statement` field was used

---

## 4) Model(s)

### 4.1 TF-IDF

- ngrams: (1, 2)
- min_df: 2
- max_df: 0.9
- other settings: default TF-IDF settings unless specified in the notebook

### 4.2 Classifier

Logistic Regression:

- max_iter: 2000
- C: default

Optional Linear SVM:

- not used in this run

---

## 5) Metrics (test split)

### 5.1 Main metrics

- **Accuracy:** 0.6196
- **Macro-F1:** 0.5935

---

### 5.2 Confusion matrix

Label order: `[real, fake]`


[[553 161]
[321 232]]


---

### 5.3 Classification report (sklearn)

          precision    recall  f1-score   support

    real      0.633     0.775     0.696       714
    fake      0.590     0.420     0.490       553

accuracy                          0.620      1267

macro avg 0.611 0.598 0.593 1267
weighted avg 0.614 0.620 0.606 1267


---

## 6) Binary mapping used in this run

Mapping rule:

- true / mostly-true / half-true → REAL (0)
- barely-true / false / pants-fire → FAKE (1)

Robustness check:

- ☐ Excluded `half-true` and re-ran

Label distribution after mapping:

REAL:

- Train: 5752
- Test: 714

FAKE:

- Train: 4488
- Test: 553

---

## 7) Interpretation

- The TF-IDF + Logistic Regression baseline achieved **moderate in-domain performance** on LIAR.
- Performance is stronger on the **real** class than on the **fake** class.
- Many fake statements were misclassified as real, suggesting that **sparse lexical features struggle to capture deceptive patterns in short political claims**.

Next steps:

- ☐ add SVM baseline
- ☐ run binary version for cross-dataset alignment
- ☑ implement a stronger baseline (e.g., BERT)

---

## 8) Validity notes

- No adaptation on test text (avoid leakage): ☑ confirmed
- This result is **in-domain (LIAR → LIAR)**. Cross-dataset ex
