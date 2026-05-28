# Cross-Dataset Model Comparison

- Date: 2026-05-12 01:29
- Source training setup: LIAR
- Target setup: FakeNewsNet minimal titles
- Transformer results are 5-seed mean/std.
- TF-IDF is deterministic, so std is reported as 0.0000.

## Combined Results

| model | target | runs | accuracy_mean | accuracy_std | macro_f1_mean | macro_f1_std | real_recall_mean | real_recall_std | fake_recall_mean | fake_recall_std | elapsed_minutes_mean |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| TF-IDF + Logistic Regression | LIAR test | 1 | 0.6235 | 0.0000 | 0.6005 | 0.0000 | 0.7661 | 0.0000 | 0.4394 | 0.0000 | nan |
| Weighted RoBERTa | LIAR test | 5 | 0.6522 | 0.0074 | 0.6396 | 0.0080 | 0.7443 | 0.0153 | 0.5335 | 0.0199 | 8.8541 |
| Weighted BERT | LIAR test | 5 | 0.6412 | 0.0065 | 0.6322 | 0.0090 | 0.7048 | 0.0292 | 0.5591 | 0.0447 | 8.7524 |
| TF-IDF + Logistic Regression | FakeNewsNet PolitiFact titles | 1 | 0.5152 | 0.0000 | 0.5146 | 0.0000 | 0.4631 | 0.0000 | 0.5903 | 0.0000 | nan |
| Weighted RoBERTa | FakeNewsNet PolitiFact titles | 5 | 0.4795 | 0.0332 | 0.4196 | 0.0529 | 0.1388 | 0.0681 | 0.9718 | 0.0177 | 8.8541 |
| Weighted BERT | FakeNewsNet PolitiFact titles | 5 | 0.4835 | 0.0453 | 0.4371 | 0.0710 | 0.1782 | 0.0995 | 0.9245 | 0.0392 | 8.7524 |
| TF-IDF + Logistic Regression | FakeNewsNet GossipCop titles | 1 | 0.4986 | 0.0000 | 0.4715 | 0.0000 | 0.4771 | 0.0000 | 0.5664 | 0.0000 | nan |
| Weighted RoBERTa | FakeNewsNet GossipCop titles | 5 | 0.2619 | 0.0145 | 0.2271 | 0.0216 | 0.0335 | 0.0230 | 0.9836 | 0.0122 | 8.8541 |
| Weighted BERT | FakeNewsNet GossipCop titles | 5 | 0.2844 | 0.0226 | 0.2601 | 0.0329 | 0.0709 | 0.0395 | 0.9589 | 0.0315 | 8.7524 |
| TF-IDF + Logistic Regression | FakeNewsNet combined titles | 1 | 0.4993 | 0.0000 | 0.4745 | 0.0000 | 0.4766 | 0.0000 | 0.5682 | 0.0000 | nan |
| Weighted RoBERTa | FakeNewsNet combined titles | 5 | 0.2718 | 0.0154 | 0.2358 | 0.0229 | 0.0372 | 0.0245 | 0.9827 | 0.0126 | 8.8541 |
| Weighted BERT | FakeNewsNet combined titles | 5 | 0.2935 | 0.0234 | 0.2682 | 0.0342 | 0.0747 | 0.0414 | 0.9564 | 0.0320 | 8.7524 |

## Key Findings

- All models drop substantially from LIAR in-domain testing to FakeNewsNet title transfer.
- TF-IDF achieves the best Macro-F1 on FakeNewsNet combined titles among the three completed transfer baselines, but it is still weak at 0.4745 Macro-F1.
- Weighted RoBERTa is best on LIAR, but transfers poorly to FakeNewsNet combined titles, with 0.2358 Macro-F1.
- Weighted BERT transfers slightly better than weighted RoBERTa on FakeNewsNet combined titles, with 0.2682 Macro-F1, but still performs poorly overall.
- The weighted transformer models strongly over-predict FAKE on FakeNewsNet titles, producing very high FAKE recall but extremely low REAL recall.

## Thesis Interpretation

The cross-dataset results support the main dissertation argument: in-domain LIAR performance does not guarantee cross-dataset reliability. The strongest in-domain model, weighted RoBERTa, is not the strongest transfer model on FakeNewsNet titles. This suggests that the transformer models may learn LIAR-specific decision boundaries that do not transfer cleanly to a different dataset and text type.

The results must be interpreted carefully because FakeNewsNet minimal uses titles rather than full article text. The experiment is therefore a short-text transfer test from LIAR statements to FakeNewsNet titles.

## Figures

- `figures/cross_dataset_model_macro_f1_comparison.png`
- `figures/cross_dataset_model_accuracy_comparison.png`
- `figures/cross_dataset_combined_recall_tradeoff.png`
