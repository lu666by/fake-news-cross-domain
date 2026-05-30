# Intermediate Fine-Tuning: LIAR -> FakeNewsNet

- Date: 2026-05-30 10:52
- Model key: `weighted_roberta`
- Seeds: `42,52,62,72,82`
- Source stage: train on LIAR train, select checkpoint by LIAR validation Macro-F1.
- Intermediate stage: continue fine-tuning on a stratified target fraction of FakeNewsNet train titles, select checkpoint by FakeNewsNet validation Macro-F1.
- Final target evaluation: held-out FakeNewsNet test titles.
- This is the main follow-up experiment after the direct LIAR -> FakeNewsNet transfer baseline.

## Compact Results

| model_key | seed | stage | target_fraction | target_train_n | test_n | accuracy | macro_f1 | real_recall | fake_recall | confusion_matrix |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| weighted_roberta | 42 | source_only_zero_shot | 0.0000 | 0 | 4640 | 0.2601 | 0.2178 | 0.0183 | 0.9930 | [[64, 3425], [8, 1143]] |
| weighted_roberta | 42 | intermediate_ft | 0.2000 | 2969 | 4640 | 0.8231 | 0.7447 | 0.9157 | 0.5421 | [[3195, 294], [527, 624]] |
| weighted_roberta | 52 | source_only_zero_shot | 0.0000 | 0 | 4640 | 0.2666 | 0.2291 | 0.0307 | 0.9818 | [[107, 3382], [21, 1130]] |
| weighted_roberta | 52 | intermediate_ft | 0.2000 | 2969 | 4640 | 0.8218 | 0.7481 | 0.9060 | 0.5665 | [[3161, 328], [499, 652]] |
| weighted_roberta | 62 | source_only_zero_shot | 0.0000 | 0 | 4640 | 0.2655 | 0.2249 | 0.0244 | 0.9965 | [[85, 3404], [4, 1147]] |
| weighted_roberta | 62 | intermediate_ft | 0.2000 | 2969 | 4640 | 0.8187 | 0.7454 | 0.9014 | 0.5682 | [[3145, 344], [497, 654]] |
| weighted_roberta | 72 | source_only_zero_shot | 0.0000 | 0 | 4640 | 0.3041 | 0.2817 | 0.0848 | 0.9687 | [[296, 3193], [36, 1115]] |
| weighted_roberta | 72 | intermediate_ft | 0.2000 | 2969 | 4640 | 0.8265 | 0.7384 | 0.9355 | 0.4961 | [[3264, 225], [580, 571]] |
| weighted_roberta | 82 | source_only_zero_shot | 0.0000 | 0 | 4640 | 0.2659 | 0.2284 | 0.0301 | 0.9809 | [[105, 3384], [22, 1129]] |
| weighted_roberta | 82 | intermediate_ft | 0.2000 | 2969 | 4640 | 0.8315 | 0.7548 | 0.9246 | 0.5491 | [[3226, 263], [519, 632]] |

## Interpretation Guide

- `source_only_zero_shot` is the original LIAR-trained model evaluated directly on FakeNewsNet test.
- `intermediate_ft` rows show whether small target-domain supervision improves FakeNewsNet performance.
- Compare Macro-F1, REAL recall, and FAKE recall together; high FAKE recall with very low REAL recall indicates a biased transfer model.
