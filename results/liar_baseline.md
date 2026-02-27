# LIAR Baseline Results

> Purpose: record the first reproducible baseline on LIAR (in-domain), with clear setup + metrics.

## 1) Run info (reproducibility)
- Date:
- Code evidence:
  - Notebook: `notebooks/02_tfidf_baseline.ipynb`
  - (Optional) Commit/PR link:
- Environment:
  - Python:
  - sklearn:
- Random seed (if used):

## 2) Dataset
- Dataset: LIAR (train/valid/test TSV)
- Text field: `statement`
- Split used for reporting: **test.tsv**
- Basic counts:
  - Train:
  - Valid:
  - Test:
- Label setting used in this run:
  - ☐ 6-class (original LIAR labels)
  - ☐ Binary (REAL/FAKE mapping; specify below)

## 3) Preprocessing
- Text cleaning:
  - ☐ strip whitespace
  - ☐ lowercasing (yes/no):
- Any filtering (e.g., remove empty statements):
- Notes:

## 4) Model(s)
### 4.1 TF-IDF
- ngrams:
- min_df:
- max_df:
- Other settings (if any):

### 4.2 Classifier
- Logistic Regression:
  - max_iter:
  - C (if changed):
- (Optional) Linear SVM:
  - C (if changed):

## 5) Metrics (test split)

### 5.1 Main metrics (report these to supervisor)
- Accuracy:
- Macro-F1:

### 5.2 Confusion matrix
> Fill after running.  
> - For binary: [[TN, FP], [FN, TP]]  
> - For 6-class: paste the matrix output and label order.

- Confusion matrix:

PASTE HERE


### 5.3 Classification report (optional but useful)
- Classification report (sklearn):

PASTE HERE


## 6) If binary mapping was used (only if applicable)
- Mapping rule:
  - true / mostly-true / half-true → REAL (1)
  - barely-true / false / pants-fire → FAKE (0)
- Any robustness check:
  - ☐ Excluded `half-true` and re-ran (record results below)
- Notes on label distribution after mapping:
  - REAL count:
  - FAKE count:

## 7) Interpretation (2–4 simple bullet points)
- In-domain baseline performance (brief):
- Any obvious error pattern (from confusion matrix):
- Next step:
  - ☐ add SVM baseline
  - ☐ run binary version (for cross-dataset alignment later)
  - ☐ start FakeNewsNet loading (later phase)

## 8) Validity notes (keep short)
- No adaptation on test text (avoid leakage): ☐ confirmed
- This result is in-domain (LIAR→LIAR). Cross-dataset experiments will be reported separately later.
