# Intermediate Fine-Tuning: LIAR -> FakeNewsNet

- Date: 2026-05-25 14:47
- Model key: `weighted_roberta`
- Seeds: `42`
- Source stage: train on LIAR train, select checkpoint by LIAR validation Macro-F1.
- Intermediate stage: continue fine-tuning on a balanced fraction of FakeNewsNet train titles, select checkpoint by FakeNewsNet validation Macro-F1.
- Final target evaluation: held-out FakeNewsNet test titles.
- This is the main follow-up experiment after the direct LIAR -> FakeNewsNet transfer baseline.

## Compact Results

| model_key | seed | stage | target_fraction | target_train_n | test_n | accuracy | macro_f1 | real_recall | fake_recall | confusion_matrix |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| weighted_roberta | 42 | source_only_zero_shot | 0.0000 | 0 | 4640 | 0.2601 | 0.2178 | 0.0183 | 0.9930 | [[64, 3425], [8, 1143]] |
| weighted_roberta | 42 | intermediate_ft | 0.2000 | 2969 | 4640 | 0.8231 | 0.7447 | 0.9157 | 0.5421 | [[3195, 294], [527, 624]] |

## Interpretation Guide

- `source_only_zero_shot` is the original LIAR-trained model evaluated directly on FakeNewsNet test.
- `intermediate_ft` rows show whether small target-domain supervision improves FakeNewsNet performance.
- Compare Macro-F1, REAL recall, and FAKE recall together; high FAKE recall with very low REAL recall indicates a biased transfer model.
