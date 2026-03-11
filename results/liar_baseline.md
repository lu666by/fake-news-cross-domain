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

## 2) Dataset
- Dataset: LIAR (train/valid/test TSV)
- Text field: `statement`
- Split used for reporting: **test.tsv**
- Basic counts:
  - Train: 10240
  - Valid: 1284
  - Test: 1267
- Label setting used in this run:
  - ☐ 6-class (original LIAR labels)
  - ☑ Binary (REAL/FAKE mapping; specified below)

## 3) Preprocessing
- Text cleaning:
  - ☑ strip whitespace
  - ☒ lowercasing (yes/no): no explicit lowercasing step
- Any filtering (e.g., remove empty statements):
  - removed empty statements
- Notes:
  - used the `statement` field only

## 4) Model(s)
### 4.1 TF-IDF
- ngrams: (1, 2)
- min_df: 2
- max_df: 0.9
- Other settings (if any):
  - default TF-IDF settings unless specified in the notebook

### 4.2 Classifier
- Logistic Regression:
  - max_iter: 2000
  - C (if changed): default
- (Optional) Linear SVM:
  - not used in this run

## 5) Metrics (test split)

### 5.1 Main metrics (report these to supervisor)
- Accuracy: 0.6196
- Macro-F1: 0.5935

### 5.2 Confusion matrix
> For binary: [[TN, FP], [FN, TP]]

- Label order: `[real, fake]`
- Confusion matrix:

```text
[[553 161]
 [321 232]]
5.3 Classification report (optional but useful)

Classification report (sklearn):

              precision    recall  f1-score   support

        real      0.633     0.775     0.696       714
        fake      0.590     0.420     0.490       553

    accuracy                          0.620      1267
   macro avg      0.611     0.598     0.593      1267
weighted avg      0.614     0.620     0.606      1267
6) Binary mapping used in this run

Mapping rule:

true / mostly-true / half-true → REAL (0)

barely-true / false / pants-fire → FAKE (1)

Any robustness check:

☐ Excluded half-true and re-ran

Notes on label distribution after mapping:

REAL count:

Train: 5752

Test: 714

FAKE count:

Train: 4488

Test: 553

7) Interpretation (2–4 simple bullet points)

The TF-IDF + Logistic Regression baseline achieved moderate in-domain performance on LIAR.

Performance was better on the real class than on the fake class.

A substantial number of fake statements were misclassified as real, suggesting that sparse lexical features are limited for detecting deceptive patterns in short political claims.

Next step:

☐ add SVM baseline

☐ run binary version (for cross-dataset alignment later)

☑ start stronger baseline modelling (e.g., BERT)

8) Validity notes (keep short)

No adaptation on test text (avoid leakage): ☑ confirmed

This result is in-domain (LIAR→LIAR). Cross-dataset experiments will be reported separately later.
