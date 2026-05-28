# Cross-Dataset Weighted BERT: LIAR to FakeNewsNet Minimal

- Date: 2026-05-12 01:27
- HuggingFace model: `bert-base-uncased`
- Seeds: `42, 52, 62, 72, 82`
- Source training data: LIAR train split
- Checkpoint selection: LIAR validation Macro-F1
- Test/evaluation targets: LIAR test, FakeNewsNet PolitiFact titles, FakeNewsNet GossipCop titles, FakeNewsNet combined titles
- Class weights: computed from LIAR train split only for each run
- Target data is never used for training or checkpoint selection

## Aggregate Results

| target | runs | accuracy_mean | accuracy_std | macro_f1_mean | macro_f1_std | real_recall_mean | real_recall_std | fake_recall_mean | fake_recall_std | elapsed_minutes_mean |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| LIAR test | 5 | 0.6412 | 0.0065 | 0.6322 | 0.0090 | 0.7048 | 0.0292 | 0.5591 | 0.0447 | 8.7524 |
| FakeNewsNet PolitiFact titles | 5 | 0.4835 | 0.0453 | 0.4371 | 0.0710 | 0.1782 | 0.0995 | 0.9245 | 0.0392 | 8.7524 |
| FakeNewsNet GossipCop titles | 5 | 0.2844 | 0.0226 | 0.2601 | 0.0329 | 0.0709 | 0.0395 | 0.9589 | 0.0315 | 8.7524 |
| FakeNewsNet combined titles | 5 | 0.2935 | 0.0234 | 0.2682 | 0.0342 | 0.0747 | 0.0414 | 0.9564 | 0.0320 | 8.7524 |

## Per-Run Results

| seed | target | best_epoch | n | accuracy | macro_f1 | real_recall | fake_recall | confusion_matrix | elapsed_minutes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 42 | LIAR test | 2 | 1267 | 0.6456 | 0.6380 | 0.7017 | 0.5732 | [[501, 213], [236, 317]] | 8.7581 |
| 42 | FakeNewsNet PolitiFact titles | 2 | 1056 | 0.4337 | 0.3545 | 0.0705 | 0.9583 | [[44, 580], [18, 414]] | 8.7581 |
| 42 | FakeNewsNet GossipCop titles | 2 | 22140 | 0.2696 | 0.2386 | 0.0448 | 0.9797 | [[753, 16064], [108, 5215]] | 8.7581 |
| 42 | FakeNewsNet combined titles | 2 | 23196 | 0.2770 | 0.2442 | 0.0457 | 0.9781 | [[797, 16644], [126, 5629]] | 8.7581 |
| 52 | LIAR test | 2 | 1267 | 0.6440 | 0.6315 | 0.7353 | 0.5262 | [[525, 189], [262, 291]] | 8.7629 |
| 52 | FakeNewsNet PolitiFact titles | 2 | 1056 | 0.5076 | 0.4715 | 0.2083 | 0.9398 | [[130, 494], [26, 406]] | 8.7629 |
| 52 | FakeNewsNet GossipCop titles | 2 | 22140 | 0.2832 | 0.2579 | 0.0649 | 0.9731 | [[1091, 15726], [143, 5180]] | 8.7629 |
| 52 | FakeNewsNet combined titles | 2 | 23196 | 0.2935 | 0.2675 | 0.0700 | 0.9706 | [[1221, 16220], [169, 5586]] | 8.7629 |
| 62 | LIAR test | 3 | 1267 | 0.6314 | 0.6218 | 0.7017 | 0.5407 | [[501, 213], [254, 299]] | 8.7424 |
| 62 | FakeNewsNet PolitiFact titles | 3 | 1056 | 0.4735 | 0.4343 | 0.1779 | 0.9005 | [[111, 513], [43, 389]] | 8.7424 |
| 62 | FakeNewsNet GossipCop titles | 3 | 22140 | 0.2929 | 0.2746 | 0.0882 | 0.9397 | [[1483, 15334], [321, 5002]] | 8.7424 |
| 62 | FakeNewsNet combined titles | 3 | 23196 | 0.3011 | 0.2819 | 0.0914 | 0.9368 | [[1594, 15847], [364, 5391]] | 8.7424 |
| 72 | LIAR test | 2 | 1267 | 0.6472 | 0.6439 | 0.6597 | 0.6311 | [[471, 243], [204, 349]] | 8.7513 |
| 72 | FakeNewsNet PolitiFact titles | 2 | 1056 | 0.4545 | 0.3889 | 0.1074 | 0.9560 | [[67, 557], [19, 413]] | 8.7513 |
| 72 | FakeNewsNet GossipCop titles | 2 | 22140 | 0.2587 | 0.2222 | 0.0277 | 0.9887 | [[465, 16352], [60, 5263]] | 8.7513 |
| 72 | FakeNewsNet combined titles | 2 | 23196 | 0.2676 | 0.2298 | 0.0305 | 0.9863 | [[532, 16909], [79, 5676]] | 8.7513 |
| 82 | LIAR test | 3 | 1267 | 0.6377 | 0.6256 | 0.7255 | 0.5244 | [[518, 196], [263, 290]] | 8.7472 |
| 82 | FakeNewsNet PolitiFact titles | 3 | 1056 | 0.5483 | 0.5361 | 0.3269 | 0.8681 | [[204, 420], [57, 375]] | 8.7472 |
| 82 | FakeNewsNet GossipCop titles | 3 | 22140 | 0.3175 | 0.3073 | 0.1289 | 0.9134 | [[2168, 14649], [461, 4862]] | 8.7472 |
| 82 | FakeNewsNet combined titles | 3 | 23196 | 0.3280 | 0.3176 | 0.1360 | 0.9100 | [[2372, 15069], [518, 5237]] | 8.7472 |

## Figures

- Metrics chart: `figures/weighted_bert_cross_dataset_metrics.png`
- Combined confusion matrix: `figures/weighted_bert_fakenewsnet_combined_confusion_matrix.png`

## Thesis Interpretation

This experiment tests whether a transformer model trained on LIAR transfers directly to FakeNewsNet minimal titles. Because FakeNewsNet minimal is title-only, the result should be described as LIAR statement to FakeNewsNet title transfer, not full-article fake news detection.
