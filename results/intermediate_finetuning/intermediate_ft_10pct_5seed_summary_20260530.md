# Intermediate Fine-Tuning 10% Rerun - 5 Seeds

- Date completed: 2026-05-30
- Model: Weighted RoBERTa (`roberta-base`)
- Seeds: 42, 52, 62, 72, 82
- Protocol: train on LIAR train, select by LIAR validation Macro-F1, continue fine-tuning on 10% of FakeNewsNet target train titles, select by FakeNewsNet validation Macro-F1, evaluate on held-out FakeNewsNet title test split.
- Target fraction: 10%
- Target train rows per seed: 1,484
- Target train label counts per seed: REAL=1,116; FAKE=368
- Important wording: the code uses a stratified 10% target fraction, not a 1:1 class-balanced subset.
- Test rows per seed: 4,640; label counts REAL=3,489, FAKE=1,151
- Text field: FakeNewsNet `title`, loaded as cleaned `text`; no full article body is used.
- Held-out split: same split function and seed protocol as the original intermediate experiment; seed 42 reproduces the original held-out setup.

## Per-seed results

|   seed |   target_train_n |   test_n |   accuracy_baseline |   macro_f1_baseline |   real_recall_baseline |   fake_recall_baseline |   accuracy |   macro_f1 |   real_recall |   fake_recall |   accuracy_uplift |   macro_f1_uplift |   real_recall_uplift |   fake_recall_uplift | confusion_matrix          |
|-------:|-----------------:|---------:|--------------------:|--------------------:|-----------------------:|-----------------------:|-----------:|-----------:|--------------:|--------------:|------------------:|------------------:|---------------------:|---------------------:|:--------------------------|
|     42 |             1484 |     4640 |              0.2601 |              0.2178 |                 0.0183 |                 0.993  |     0.8116 |     0.7203 |        0.9197 |        0.4839 |            0.5515 |            0.5024 |               0.9014 |              -0.5091 | [[3209, 280], [594, 557]] |
|     52 |             1484 |     4640 |              0.2666 |              0.2291 |                 0.0307 |                 0.9818 |     0.8    |     0.6523 |        0.9653 |        0.2989 |            0.5334 |            0.4232 |               0.9347 |              -0.6829 | [[3368, 121], [807, 344]] |
|     62 |             1484 |     4640 |              0.2655 |              0.2249 |                 0.0244 |                 0.9965 |     0.8121 |     0.7195 |        0.922  |        0.4787 |            0.5466 |            0.4945 |               0.8977 |              -0.5178 | [[3217, 272], [600, 551]] |
|     72 |             1484 |     4640 |              0.3041 |              0.2817 |                 0.0848 |                 0.9687 |     0.8022 |     0.7018 |        0.9192 |        0.4474 |            0.4981 |            0.4201 |               0.8343 |              -0.5213 | [[3207, 282], [636, 515]] |
|     82 |             1484 |     4640 |              0.2659 |              0.2284 |                 0.0301 |                 0.9809 |     0.8157 |     0.7236 |        0.9263 |        0.4805 |            0.5498 |            0.4952 |               0.8962 |              -0.5004 | [[3232, 257], [598, 553]] |

## Mean / std / range for 10% fine-tuning

| row   |   accuracy |   macro_f1 |   real_recall |   fake_recall |   accuracy_uplift |   macro_f1_uplift |   real_recall_uplift |   fake_recall_uplift |
|:------|-----------:|-----------:|--------------:|--------------:|------------------:|------------------:|---------------------:|---------------------:|
| mean  |     0.8083 |     0.7035 |        0.9305 |        0.4379 |            0.5359 |            0.4671 |               0.8929 |              -0.5463 |
| std   |     0.0068 |     0.0298 |        0.0197 |        0.0791 |            0.0223 |            0.0416 |               0.0363 |               0.0768 |
| min   |     0.8    |     0.6523 |        0.9192 |        0.2989 |            0.4981 |            0.4201 |               0.8343 |              -0.6829 |
| max   |     0.8157 |     0.7236 |        0.9653 |        0.4839 |            0.5515 |            0.5024 |               0.9347 |              -0.5004 |

## Comparison with source-only direct baseline

| row                  |   accuracy |   macro_f1 |   real_recall |   fake_recall |
|:---------------------|-----------:|-----------:|--------------:|--------------:|
| direct baseline mean |     0.2725 |     0.2364 |        0.0377 |        0.9842 |
| direct baseline std  |     0.0179 |     0.0257 |        0.0268 |        0.011  |
| 10% FT mean          |     0.8083 |     0.7035 |        0.9305 |        0.4379 |
| 10% FT std           |     0.0068 |     0.0298 |        0.0197 |        0.0791 |
| mean uplift          |     0.5359 |     0.4671 |        0.8929 |       -0.5463 |

## Initial interpretation

Across five seeds, 10% intermediate fine-tuning improves Macro-F1 from the source-only baseline mean 0.2364 (std 0.0257) to 0.7035 (std 0.0298), an average uplift of 0.4671.
Every seed improves over its paired source-only direct baseline, and even the weakest 10% run (0.6523) is far above the strongest direct-transfer baseline run (0.2817).
The improvement is therefore stable enough to support the thesis claim that a small amount of target-domain title supervision substantially reduces the direct-transfer failure. The remaining caveat is that the 10% target subset is stratified rather than 1:1 balanced, so the wording in the thesis table should avoid saying simply "balanced" unless the sampling is changed.
