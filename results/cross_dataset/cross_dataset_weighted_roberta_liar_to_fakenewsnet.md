# Cross-Dataset Weighted RoBERTa: LIAR to FakeNewsNet Minimal

- Date: 2026-05-12 00:23
- HuggingFace model: `roberta-base`
- Seeds: `42, 52, 62, 72, 82`
- Source training data: LIAR train split
- Checkpoint selection: LIAR validation Macro-F1
- Test/evaluation targets: LIAR test, FakeNewsNet PolitiFact titles, FakeNewsNet GossipCop titles, FakeNewsNet combined titles
- Class weights: computed from LIAR train split only for each run
- Target data is never used for training or checkpoint selection

## Aggregate Results

| target | runs | accuracy_mean | accuracy_std | macro_f1_mean | macro_f1_std | real_recall_mean | real_recall_std | fake_recall_mean | fake_recall_std | elapsed_minutes_mean |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| LIAR test | 5 | 0.6522 | 0.0074 | 0.6396 | 0.0080 | 0.7443 | 0.0153 | 0.5335 | 0.0199 | 8.8541 |
| FakeNewsNet PolitiFact titles | 5 | 0.4795 | 0.0332 | 0.4196 | 0.0529 | 0.1388 | 0.0681 | 0.9718 | 0.0177 | 8.8541 |
| FakeNewsNet GossipCop titles | 5 | 0.2619 | 0.0145 | 0.2271 | 0.0216 | 0.0335 | 0.0230 | 0.9836 | 0.0122 | 8.8541 |
| FakeNewsNet combined titles | 5 | 0.2718 | 0.0154 | 0.2358 | 0.0229 | 0.0372 | 0.0245 | 0.9827 | 0.0126 | 8.8541 |

## Per-Run Results

| seed | target | best_epoch | n | accuracy | macro_f1 | real_recall | fake_recall | confusion_matrix | elapsed_minutes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 42 | LIAR test | 3 | 1267 | 0.6535 | 0.6408 | 0.7465 | 0.5335 | [[533, 181], [258, 295]] | 8.9519 |
| 42 | FakeNewsNet PolitiFact titles | 3 | 1056 | 0.4631 | 0.3920 | 0.1026 | 0.9838 | [[64, 560], [7, 425]] | 8.9519 |
| 42 | FakeNewsNet GossipCop titles | 3 | 22140 | 0.2506 | 0.2097 | 0.0152 | 0.9942 | [[256, 16561], [31, 5292]] | 8.9519 |
| 42 | FakeNewsNet combined titles | 3 | 23196 | 0.2603 | 0.2179 | 0.0183 | 0.9934 | [[320, 17121], [38, 5717]] | 8.9519 |
| 52 | LIAR test | 3 | 1267 | 0.6606 | 0.6496 | 0.7437 | 0.5533 | [[531, 183], [247, 306]] | 8.8095 |
| 52 | FakeNewsNet PolitiFact titles | 3 | 1056 | 0.4697 | 0.4076 | 0.1234 | 0.9699 | [[77, 547], [13, 419]] | 8.8095 |
| 52 | FakeNewsNet GossipCop titles | 3 | 22140 | 0.2584 | 0.2228 | 0.0291 | 0.9829 | [[490, 16327], [91, 5232]] | 8.8095 |
| 52 | FakeNewsNet combined titles | 3 | 23196 | 0.2681 | 0.2311 | 0.0325 | 0.9819 | [[567, 16874], [104, 5651]] | 8.8095 |
| 62 | LIAR test | 2 | 1267 | 0.6504 | 0.6403 | 0.7255 | 0.5533 | [[518, 196], [247, 306]] | 8.8076 |
| 62 | FakeNewsNet PolitiFact titles | 2 | 1056 | 0.4527 | 0.3741 | 0.0833 | 0.9861 | [[52, 572], [6, 426]] | 8.8076 |
| 62 | FakeNewsNet GossipCop titles | 2 | 22140 | 0.2544 | 0.2155 | 0.0209 | 0.9923 | [[351, 16466], [41, 5282]] | 8.8076 |
| 62 | FakeNewsNet combined titles | 2 | 23196 | 0.2635 | 0.2228 | 0.0231 | 0.9918 | [[403, 17038], [47, 5708]] | 8.8076 |
| 72 | LIAR test | 3 | 1267 | 0.6559 | 0.6401 | 0.7675 | 0.5118 | [[548, 166], [270, 283]] | 8.8550 |
| 72 | FakeNewsNet PolitiFact titles | 3 | 1056 | 0.5369 | 0.5101 | 0.2564 | 0.9421 | [[160, 464], [25, 407]] | 8.8550 |
| 72 | FakeNewsNet GossipCop titles | 3 | 22140 | 0.2872 | 0.2644 | 0.0732 | 0.9634 | [[1231, 15586], [195, 5128]] | 8.8550 |
| 72 | FakeNewsNet combined titles | 3 | 23196 | 0.2986 | 0.2755 | 0.0798 | 0.9618 | [[1391, 16050], [220, 5535]] | 8.8550 |
| 82 | LIAR test | 3 | 1267 | 0.6409 | 0.6273 | 0.7381 | 0.5154 | [[527, 187], [268, 285]] | 8.8466 |
| 82 | FakeNewsNet PolitiFact titles | 3 | 1056 | 0.4754 | 0.4139 | 0.1282 | 0.9769 | [[80, 544], [10, 422]] | 8.8466 |
| 82 | FakeNewsNet GossipCop titles | 3 | 22140 | 0.2588 | 0.2229 | 0.0288 | 0.9852 | [[485, 16332], [79, 5244]] | 8.8466 |
| 82 | FakeNewsNet combined titles | 3 | 23196 | 0.2686 | 0.2315 | 0.0324 | 0.9845 | [[565, 16876], [89, 5666]] | 8.8466 |

## Figures

- Metrics chart: `figures/weighted_roberta_cross_dataset_metrics.png`
- Combined confusion matrix: `figures/weighted_roberta_fakenewsnet_combined_confusion_matrix.png`

## Thesis Interpretation

This experiment tests whether a transformer model trained on LIAR transfers directly to FakeNewsNet minimal titles. Because FakeNewsNet minimal is title-only, the result should be described as LIAR statement to FakeNewsNet title transfer, not full-article fake news detection.
