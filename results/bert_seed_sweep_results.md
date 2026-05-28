# BERT Seed Sweep Results

- Notebook source: `03_bert_baseline.ipynb`
- Dataset: LIAR (`liar_dataset/train.tsv`, `valid.tsv`, `test.tsv`)
- Model: `bert-base-uncased`
- Seeds: `42`, `52`, `62`, `72`, `82`
- Checkpoint selection: best validation macro-F1
- Note: standard deviation is sample std with `ddof=1`

## Per-run and aggregate results

| seed | best_epoch | valid_accuracy | valid_macro_f1 | test_accuracy | test_macro_f1 | training_minutes |
| --- | --- | --- | --- | --- | --- | --- |
| 42 | 2 | 0.6386 | 0.6309 | 0.6401 | 0.6231 | 8.9055 |
| 52 | 3 | 0.6472 | 0.6387 | 0.6346 | 0.6132 | 8.9433 |
| 62 | 3 | 0.6394 | 0.6288 | 0.6361 | 0.6145 | 8.8996 |
| 72 | 2 | 0.6433 | 0.6344 | 0.6433 | 0.6210 | 8.6957 |
| 82 | 2 | 0.6456 | 0.6405 | 0.6582 | 0.6435 | 8.6955 |
| mean |  | 0.6428 | 0.6346 | 0.6425 | 0.6231 | 8.8279 |
| std |  | 0.0038 | 0.0050 | 0.0095 | 0.0122 | 0.1219 |

## Comparison vs previous 3-seed mean

| metric | previous_3_seed_mean | new_5_run_mean | delta |
| --- | --- | --- | --- |
| validation_accuracy | 0.6417 | 0.6428 | +0.0011 |
| validation_macro_f1 | 0.6328 | 0.6346 | +0.0019 |
| test_accuracy | 0.6369 | 0.6425 | +0.0055 |
| test_macro_f1 | 0.6169 | 0.6231 | +0.0061 |
