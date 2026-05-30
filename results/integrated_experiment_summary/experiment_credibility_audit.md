# Experiment Credibility Audit

- Date: 2026-05-25
- Scope: intermediate fine-tuning split integrity, label mapping, and metric consistency checks.

## A. Split Integrity

- FakeNewsNet split seed: `42`
- Split sizes: train `14844`, validation `3712`, held-out test `4640`
- Train/test id overlap: `0`
- Validation/test id overlap: `0`
- Intermediate fine-tuning uses only `fnn_train` subsets; checkpoint selection uses `fnn_valid`; final evaluation uses `fnn_test`.

| Target fraction | Sample n | REAL n | FAKE n | Overlap with test ids | Non-train ids |
|---:|---:|---:|---:|---:|---:|
| 0.05 | 742 | 558 | 184 | 0 | 0 |
| 0.10 | 1484 | 1116 | 368 | 0 | 0 |
| 0.20 | 2969 | 2232 | 737 | 0 | 0 |

Conclusion: the 5%, 10%, and 20% target-domain samples are drawn from the FakeNewsNet train split only, and the held-out FakeNewsNet test split is not used for intermediate fine-tuning.

## B. Label Mapping

- Project-wide binary mapping is `REAL=0`, `FAKE=1`.
- FakeNewsNet loader maps fake CSV files to `y=1` and real CSV files to `y=0`.
- Confusion matrices are read as `[[REAL->REAL, REAL->FAKE], [FAKE->REAL, FAKE->FAKE]]`.

## C. Metric Consistency

| Setting | Accuracy ok | Macro-F1 ok | REAL recall ok | FAKE recall ok |
|---|---|---|---|---|
| LIAR -> held-out FakeNewsNet test | True | True | True | True |
| LIAR -> 5% FNN train -> FNN test | True | True | True | True |
| LIAR -> 10% FNN train -> FNN test | True | True | True | True |
| LIAR -> 20% FNN train -> FNN test | True | True | True | True |
| LLM atoms: LIAR atoms -> FakeNewsNet atoms | True | True | True | True |
| LLM atoms: FakeNewsNet atoms -> FakeNewsNet atoms | True | True | True | True |

Conclusion: checked rows match their confusion matrices within rounding tolerance. The 10% and 20% improvements are not explained by test leakage; they are produced after target-domain intermediate fine-tuning on training split subsets and evaluation on the same held-out test split.