# Weighted BERT Seed Sweep Results

- Notebook source: `04_bert_weighted_baseline.ipynb`
- Dataset: LIAR (`liar_dataset/train.tsv`, `valid.tsv`, `test.tsv`)
- Model: `bert-base-uncased` with weighted training loss
- Seeds: `42`, `52`, `62`, `72`, `82`
- Checkpoint selection: best validation macro-F1
- Note: standard deviation is sample std with `ddof=1`

## Per-run and aggregate table

| seed | best_epoch | valid_accuracy | valid_macro_f1 | test_accuracy | test_macro_f1 | real_recall | fake_recall | training_minutes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 42 | 2 | 0.6425 | 0.6407 | 0.6456 | 0.6380 | 0.7017 | 0.5732 | 7.5001 |
| 52 | 2 | 0.6456 | 0.6421 | 0.6440 | 0.6315 | 0.7353 | 0.5262 | 7.5124 |
| 62 | 3 | 0.6550 | 0.6519 | 0.6314 | 0.6218 | 0.7017 | 0.5407 | 7.5194 |
| 72 | 2 | 0.6456 | 0.6451 | 0.6472 | 0.6439 | 0.6597 | 0.6311 | 7.5583 |
| 82 | 3 | 0.6472 | 0.6444 | 0.6377 | 0.6256 | 0.7255 | 0.5244 | 7.5598 |
| mean |  | 0.6472 | 0.6448 | 0.6412 | 0.6322 | 0.7048 | 0.5591 | 7.5300 |
| std |  | 0.0047 | 0.0043 | 0.0065 | 0.0090 | 0.0292 | 0.0447 | 0.0274 |

## Baseline comparison

| baseline | test_accuracy | test_macro_f1 | accuracy_delta_vs_weighted_mean | macro_f1_delta_vs_weighted_mean |
| --- | --- | --- | --- | --- |
| Weighted BERT mean | 0.6412 | 0.6322 | 0.0000 | 0.0000 |
| Unweighted BERT 5-run mean | 0.6425 | 0.6231 | 0.0013 | -0.0091 |
| TF-IDF baseline | 0.6235 | 0.6005 | -0.0177 | -0.0317 |
| RoBERTa baseline | 0.6504 | 0.6262 | 0.0092 | -0.0060 |