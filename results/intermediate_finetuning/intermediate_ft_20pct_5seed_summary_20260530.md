# Intermediate Fine-Tuning 20% Five-Seed Summary (2026-05-30)

## Scope

- Model: weighted RoBERTa.
- Seeds: 42, 52, 62, 72, 82.
- Target fraction: 20% stratified FakeNewsNet target-train titles.
- Target train size: 2969 rows for every seed.
- Held-out test size: 4640 rows.
- Training protocol: same seed set and source/target epoch protocol as the 10% rerun.

## Per-Seed Results

|   seed |   target_train_n |   test_n |   accuracy |   macro_f1 |   real_recall |   fake_recall |   accuracy_uplift |   macro_f1_uplift |   real_recall_uplift |   fake_recall_uplift | confusion_matrix          |
|-------:|-----------------:|---------:|-----------:|-----------:|--------------:|--------------:|------------------:|------------------:|---------------------:|---------------------:|:--------------------------|
|     42 |             2969 |     4640 |     0.8231 |     0.7447 |        0.9157 |        0.5421 |            0.5629 |            0.5268 |               0.8974 |              -0.4509 | [[3195, 294], [527, 624]] |
|     52 |             2969 |     4640 |     0.8218 |     0.7481 |        0.906  |        0.5665 |            0.5552 |            0.519  |               0.8753 |              -0.4153 | [[3161, 328], [499, 652]] |
|     62 |             2969 |     4640 |     0.8188 |     0.7454 |        0.9014 |        0.5682 |            0.5532 |            0.5204 |               0.877  |              -0.4283 | [[3145, 344], [497, 654]] |
|     72 |             2969 |     4640 |     0.8265 |     0.7384 |        0.9355 |        0.4961 |            0.5224 |            0.4567 |               0.8507 |              -0.4726 | [[3264, 225], [580, 571]] |
|     82 |             2969 |     4640 |     0.8315 |     0.7548 |        0.9246 |        0.5491 |            0.5655 |            0.5265 |               0.8945 |              -0.4318 | [[3226, 263], [519, 632]] |

## 20% Mean / Std / Min / Max

| row   |   accuracy |   macro_f1 |   real_recall |   fake_recall |   accuracy_uplift |   macro_f1_uplift |   real_recall_uplift |   fake_recall_uplift |
|:------|-----------:|-----------:|--------------:|--------------:|------------------:|------------------:|---------------------:|---------------------:|
| mean  |     0.8243 |     0.7463 |        0.9167 |        0.5444 |            0.5519 |            0.5099 |               0.879  |              -0.4398 |
| std   |     0.0049 |     0.006  |        0.0138 |        0.0292 |            0.0172 |            0.03   |               0.0187 |               0.0223 |
| min   |     0.8188 |     0.7384 |        0.9014 |        0.4961 |            0.5224 |            0.4567 |               0.8507 |              -0.4726 |
| max   |     0.8315 |     0.7548 |        0.9355 |        0.5682 |            0.5655 |            0.5268 |               0.8974 |              -0.4153 |

## Comparison with Direct Baseline and 10%

| condition                   | evidence   |   accuracy |   macro_f1 |   real_recall |   fake_recall |
|:----------------------------|:-----------|-----------:|-----------:|--------------:|--------------:|
| Direct titles-only baseline | 5 seeds    |     0.2725 |     0.2364 |        0.0377 |        0.9842 |
| Intermediate FT 10%         | 5 seeds    |     0.8083 |     0.7035 |        0.9305 |        0.4379 |
| Intermediate FT 20%         | 5 seeds    |     0.8243 |     0.7463 |        0.9167 |        0.5444 |

## Reading

The 20% intermediate fine-tuning rerun is no longer a seed-42-only result. Across five seeds it reaches mean Accuracy 0.8243 +/- 0.0049 and mean Macro-F1 0.7463 +/- 0.0060. Relative to the direct titles-only baseline, the mean Macro-F1 uplift is 0.5099. Compared with the 10% rerun, 20% improves mean Macro-F1 from 0.7035 to 0.7463 and mean FAKE recall from 0.4379 to 0.5444, while REAL recall is slightly lower (0.9305 -> 0.9167).

Preliminary thesis framing: 10% is the more data-efficient result, while 20% is currently the strongest absolute five-seed intermediate fine-tuning setting. The supervisor-facing question is whether to emphasize efficiency (10%) or best absolute performance (20%).
