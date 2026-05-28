# Cross-Dataset Unweighted BERT: LIAR to FakeNewsNet Minimal

- Date: 2026-05-14 15:30
- HuggingFace model: `bert-base-uncased`
- Seeds: `42, 52, 62, 72, 82`
- Source training data: LIAR train split
- Checkpoint selection: LIAR validation Macro-F1
- Test/evaluation targets: LIAR test, FakeNewsNet PolitiFact titles, FakeNewsNet GossipCop titles, FakeNewsNet combined titles
- Class weights: None (unweighted cross-entropy)
- Target data is never used for training or checkpoint selection

## Aggregate Results

| target | runs | accuracy_mean | accuracy_std | macro_f1_mean | macro_f1_std | real_recall_mean | real_recall_std | fake_recall_mean | fake_recall_std | elapsed_minutes_mean |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| LIAR test | 5 | 0.6425 | 0.0095 | 0.6231 | 0.0122 | 0.7706 | 0.0110 | 0.4770 | 0.0281 | 8.9522 |
| FakeNewsNet PolitiFact titles | 5 | 0.5114 | 0.0560 | 0.4805 | 0.0803 | 0.2436 | 0.1135 | 0.8981 | 0.0333 | 8.9522 |
| FakeNewsNet GossipCop titles | 5 | 0.2918 | 0.0185 | 0.2710 | 0.0266 | 0.0832 | 0.0335 | 0.9507 | 0.0293 | 8.9522 |
| FakeNewsNet combined titles | 5 | 0.3018 | 0.0191 | 0.2806 | 0.0275 | 0.0890 | 0.0349 | 0.9467 | 0.0294 | 8.9522 |

## Per-Run Results

| seed | target | best_epoch | n | accuracy | macro_f1 | real_recall | fake_recall | confusion_matrix | elapsed_minutes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 42 | LIAR test | 2 | 1267 | 0.6401 | 0.6231 | 0.7563 | 0.4901 | [[540, 174], [282, 271]] | 9.1439 |
| 42 | FakeNewsNet PolitiFact titles | 2 | 1056 | 0.4356 | 0.3695 | 0.0946 | 0.9282 | [[59, 565], [31, 401]] | 9.1439 |
| 42 | FakeNewsNet GossipCop titles | 2 | 22140 | 0.2883 | 0.2659 | 0.0749 | 0.9622 | [[1260, 15557], [201, 5122]] | 9.1439 |
| 42 | FakeNewsNet combined titles | 2 | 23196 | 0.2950 | 0.2710 | 0.0756 | 0.9597 | [[1319, 16122], [232, 5523]] | 9.1439 |
| 52 | LIAR test | 3 | 1267 | 0.6346 | 0.6132 | 0.7717 | 0.4575 | [[551, 163], [300, 253]] | 9.0269 |
| 52 | FakeNewsNet PolitiFact titles | 3 | 1056 | 0.5720 | 0.5619 | 0.3558 | 0.8843 | [[222, 402], [50, 382]] | 9.0269 |
| 52 | FakeNewsNet GossipCop titles | 3 | 22140 | 0.2886 | 0.2671 | 0.0773 | 0.9562 | [[1300, 15517], [233, 5090]] | 9.0269 |
| 52 | FakeNewsNet combined titles | 3 | 23196 | 0.3015 | 0.2807 | 0.0873 | 0.9508 | [[1522, 15919], [283, 5472]] | 9.0269 |
| 62 | LIAR test | 3 | 1267 | 0.6361 | 0.6145 | 0.7745 | 0.4575 | [[553, 161], [300, 253]] | 8.9900 |
| 62 | FakeNewsNet PolitiFact titles | 3 | 1056 | 0.5473 | 0.5375 | 0.3397 | 0.8472 | [[212, 412], [66, 366]] | 8.9900 |
| 62 | FakeNewsNet GossipCop titles | 3 | 22140 | 0.3194 | 0.3104 | 0.1350 | 0.9019 | [[2270, 14547], [522, 4801]] | 8.9900 |
| 62 | FakeNewsNet combined titles | 3 | 23196 | 0.3298 | 0.3207 | 0.1423 | 0.8978 | [[2482, 14959], [588, 5167]] | 8.9900 |
| 72 | LIAR test | 2 | 1267 | 0.6433 | 0.6210 | 0.7857 | 0.4593 | [[561, 153], [299, 254]] | 8.8859 |
| 72 | FakeNewsNet PolitiFact titles | 2 | 1056 | 0.4725 | 0.4266 | 0.1603 | 0.9236 | [[100, 524], [33, 399]] | 8.8859 |
| 72 | FakeNewsNet GossipCop titles | 2 | 22140 | 0.2678 | 0.2360 | 0.0421 | 0.9807 | [[708, 16109], [103, 5220]] | 8.8859 |
| 72 | FakeNewsNet combined titles | 2 | 23196 | 0.2771 | 0.2446 | 0.0463 | 0.9764 | [[808, 16633], [136, 5619]] | 8.8859 |
| 82 | LIAR test | 2 | 1267 | 0.6582 | 0.6435 | 0.7647 | 0.5208 | [[546, 168], [265, 288]] | 8.7144 |
| 82 | FakeNewsNet PolitiFact titles | 2 | 1056 | 0.5294 | 0.5070 | 0.2676 | 0.9074 | [[167, 457], [40, 392]] | 8.7144 |
| 82 | FakeNewsNet GossipCop titles | 2 | 22140 | 0.2949 | 0.2757 | 0.0869 | 0.9523 | [[1461, 15356], [254, 5069]] | 8.7144 |
| 82 | FakeNewsNet combined titles | 2 | 23196 | 0.3056 | 0.2861 | 0.0933 | 0.9489 | [[1628, 15813], [294, 5461]] | 8.7144 |

## Figures

- Metrics chart: `figures/unweighted_bert_cross_dataset_metrics.png`
- Combined confusion matrix: `figures/unweighted_bert_fakenewsnet_combined_confusion_matrix.png`

## Thesis Interpretation

This experiment tests whether a transformer model trained on LIAR transfers directly to FakeNewsNet minimal titles. Because FakeNewsNet minimal is title-only, the result should be described as LIAR statement to FakeNewsNet title transfer, not full-article fake news detection.
