# TF-IDF Determinism Check (5 Seeds)

- Source baseline: `02_tfidf_baseline_v2.ipynb` selected configuration
- Selected configuration: `P0_minimal`, `ngram_range=(1,2)`, `min_df=2`, `max_df=1.0`, `LogisticRegression(max_iter=2000, C=1.0)`
- Purpose: verify whether changing `random_state` changes the current TF-IDF baseline in practice

| seed | validation_accuracy | validation_macro_f1 | test_accuracy | test_macro_f1 | confusion_matrix | prediction_hash |
| --- | --- | --- | --- | --- | --- | --- |
| 42 | 0.6231 | 0.6123 | 0.6235 | 0.6005 | [[547, 167], [310, 243]] | 6c39052eff8c0d20 |
| 52 | 0.6231 | 0.6123 | 0.6235 | 0.6005 | [[547, 167], [310, 243]] | 6c39052eff8c0d20 |
| 62 | 0.6231 | 0.6123 | 0.6235 | 0.6005 | [[547, 167], [310, 243]] | 6c39052eff8c0d20 |
| 72 | 0.6231 | 0.6123 | 0.6235 | 0.6005 | [[547, 167], [310, 243]] | 6c39052eff8c0d20 |
| 82 | 0.6231 | 0.6123 | 0.6235 | 0.6005 | [[547, 167], [310, 243]] | 6c39052eff8c0d20 |
| mean | 0.6231 | 0.6123 | 0.6235 | 0.6005 |  |  |
| std | 0.0000 | 0.0000 | 0.0000 | 0.0000 |  |  |
