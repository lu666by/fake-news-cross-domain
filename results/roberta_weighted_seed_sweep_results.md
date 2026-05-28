# Weighted RoBERTa Seed Sweep Results

- Notebook source: `06_roberta_weighted_baseline.ipynb`
- Dataset: LIAR (`liar_dataset/train.tsv`, `valid.tsv`, `test.tsv`)
- Model: `roberta-base` with weighted training loss
- Seeds: `42`, `52`, `62`, `72`, `82`
- Checkpoint selection: best validation macro-F1
- Note: standard deviation is sample std with `ddof=1`

## Per-run and aggregate table

| seed | best_epoch | valid_accuracy | valid_macro_f1 | test_accuracy | test_macro_f1 | real_recall | fake_recall | confusion_matrix | training_minutes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 42 | 3 | 0.6713 | 0.6668 | 0.6535 | 0.6408 | 0.7465 | 0.5335 | [[533, 181], [258, 295]] | 7.6488 |
| 52 | 3 | 0.6604 | 0.6573 | 0.6606 | 0.6496 | 0.7437 | 0.5533 | [[531, 183], [247, 306]] | 7.6607 |
| 62 | 2 | 0.6558 | 0.6528 | 0.6504 | 0.6403 | 0.7255 | 0.5533 | [[518, 196], [247, 306]] | 7.6565 |
| 72 | 3 | 0.6636 | 0.6577 | 0.6559 | 0.6401 | 0.7675 | 0.5118 | [[548, 166], [270, 283]] | 7.6608 |
| 82 | 3 | 0.6674 | 0.6629 | 0.6409 | 0.6273 | 0.7381 | 0.5154 | [[527, 187], [268, 285]] | 7.6659 |
| mean |  | 0.6637 | 0.6595 | 0.6522 | 0.6396 | 0.7443 | 0.5335 |  | 7.6585 |
| std |  | 0.0060 | 0.0054 | 0.0074 | 0.0080 | 0.0153 | 0.0199 |  | 0.0064 |

## Baseline comparison

| baseline | test_accuracy | test_macro_f1 | accuracy_delta_vs_weighted_roberta_mean | macro_f1_delta_vs_weighted_roberta_mean |
| --- | --- | --- | --- | --- |
| Weighted RoBERTa mean | 0.6522 | 0.6396 | 0.0000 | 0.0000 |
| TF-IDF baseline | 0.6235 | 0.6005 | -0.0287 | -0.0391 |
| Unweighted BERT 5-run mean | 0.6425 | 0.6231 | -0.0098 | -0.0166 |
| Weighted BERT 5-run mean | 0.6412 | 0.6322 | -0.0110 | -0.0075 |
| Unweighted RoBERTa single-run | 0.6504 | 0.6262 | -0.0018 | -0.0134 |
