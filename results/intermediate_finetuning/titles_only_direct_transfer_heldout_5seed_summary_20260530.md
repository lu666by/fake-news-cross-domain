# Titles-only Direct Transfer Baseline Rerun - 5 Seeds

- Date completed: 2026-05-30
- Model: Weighted RoBERTa (`roberta-base`)
- Protocol: train on LIAR train, select source checkpoint by LIAR validation Macro-F1, evaluate direct zero-shot on held-out FakeNewsNet title test split.
- Seeds: 42, 52, 62, 72, 82
- Target-domain training rows: 0
- Test rows per seed: 4,640
- Command output source: `intermediate_finetuning_weighted_roberta_seeds_42_52_62_72_82_fractions__full.csv`

## Per-seed results

|   seed |   test_n |   accuracy |   macro_f1 |   real_recall |   fake_recall | confusion_matrix          |
|-------:|---------:|-----------:|-----------:|--------------:|--------------:|:--------------------------|
|     42 |     4640 |     0.2601 |     0.2178 |        0.0183 |        0.993  | [[64, 3425], [8, 1143]]   |
|     52 |     4640 |     0.2666 |     0.2291 |        0.0307 |        0.9818 | [[107, 3382], [21, 1130]] |
|     62 |     4640 |     0.2655 |     0.2249 |        0.0244 |        0.9965 | [[85, 3404], [4, 1147]]   |
|     72 |     4640 |     0.3041 |     0.2817 |        0.0848 |        0.9687 | [[296, 3193], [36, 1115]] |
|     82 |     4640 |     0.2659 |     0.2284 |        0.0301 |        0.9809 | [[105, 3384], [22, 1129]] |

## Mean / std

| row   |   accuracy |   macro_f1 |   real_recall |   fake_recall |
|:------|-----------:|-----------:|--------------:|--------------:|
| mean  |     0.2725 |     0.2364 |        0.0377 |        0.9842 |
| std   |     0.0179 |     0.0257 |        0.0268 |        0.011  |
| min   |     0.2601 |     0.2178 |        0.0183 |        0.9687 |
| max   |     0.3041 |     0.2817 |        0.0848 |        0.9965 |

## Comparison with original seed-42 single run

| item                    |   accuracy |   macro_f1 |   real_recall |   fake_recall |
|:------------------------|-----------:|-----------:|--------------:|--------------:|
| old seed-42 single run  |     0.2601 |     0.2178 |        0.0183 |        0.993  |
| new 5-seed mean         |     0.2725 |     0.2364 |        0.0377 |        0.9842 |
| difference mean - old42 |     0.0124 |     0.0186 |        0.0194 |       -0.0088 |

## Comparison with existing combined-title 5-seed baseline

| item | accuracy | macro_f1 | real_recall | fake_recall |
|:---|---:|---:|---:|---:|
| Existing combined titles 5-seed mean | 0.2718 | 0.2358 | 0.0372 | 0.9827 |
| New held-out title test 5-seed mean | 0.2725 | 0.2364 | 0.0377 | 0.9842 |

The two title-only direct-transfer summaries are effectively the same. The held-out split is not showing a meaningful improvement over the existing combined-title evaluation; both expose the same severe FAKE-biased transfer failure.

## Answer for supervisor

The original seed-42 result is not an unusually strong lucky run. Its Macro-F1 (0.2178) is slightly below the new 5-seed mean (0.2364) and well within the observed range (0.2178-0.2817).
However, the 5-seed results remain very poor overall: mean Accuracy 0.2725, mean Macro-F1 0.2364, mean REAL recall 0.0377, and mean FAKE recall 0.9842. The model still heavily over-predicts FAKE on FakeNewsNet titles.
So the safe conclusion is: titles-only direct transfer is consistently weak; seed choice changes the exact number, but it does not change the failure pattern.
