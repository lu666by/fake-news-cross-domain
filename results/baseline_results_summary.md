# LIAR Baseline Results Summary

## Task
This file summarises the current **in-domain binary fake news detection baselines** on the **LIAR** dataset.

The project uses the following binary label mapping:

- **REAL (0):** `true`, `mostly-true`, `half-true`
- **FAKE (1):** `barely-true`, `false`, `pants-fire`

All current baseline experiments use **statement** as the main input text.

## Dataset
Split sizes:

- **Train:** 10240
- **Valid:** 1284
- **Test:** 1267

## Baseline development path
The baseline development progressed through the following stages:

1. **TF-IDF + Logistic Regression**
2. **BERT-base**
3. **BERT-base + weighted loss**
4. **RoBERTa-base**

## Main results

| Model | Accuracy | Macro-F1 | Notes |
|---|---:|---:|---|
| TF-IDF + Logistic Regression | 0.6235 | 0.6005 | Final sparse baseline |
| BERT-base (3-seed mean) | 0.6369 ± 0.0028 | 0.6169 ± 0.0054 | Mean over seeds 42, 52, 62 |
| BERT-base + weighted loss (3-seed mean) | 0.6404 ± 0.0078 | 0.6304 ± 0.0081 | Mean over seeds 42, 52, 62 |
| RoBERTa-base (single run) | 0.6504 | 0.6262 | Single run only |

## Current primary model
The current **primary model** is **BERT-base with weighted loss**.

This is the most suitable main model for the current study because:

- it achieves the **best mean Macro-F1** among the tested models,
- it improves over the unweighted BERT baseline,
- it provides better balance between the **REAL** and **FAKE** classes,
- it is more appropriate than RoBERTa when **class-balanced performance** is prioritised over raw accuracy alone.

## Weighted BERT (current main result)
The weighted BERT baseline was run with **3 random seeds**: `42`, `52`, and `62`.

### Mean and standard deviation
- **Validation Accuracy:** `0.6477 ± 0.0065`
- **Validation Macro-F1:** `0.6449 ± 0.0061`
- **Test Accuracy:** `0.6404 ± 0.0078`
- **Test Macro-F1:** `0.6304 ± 0.0081`
- **REAL Recall:** `0.7129 ± 0.0194`
- **FAKE Recall:** `0.5467 ± 0.0241`

## Comparison with earlier baselines

### Weighted BERT vs TF-IDF
- **Accuracy delta:** `+0.0169`
- **Macro-F1 delta:** `+0.0299`

### Weighted BERT vs unweighted BERT
- **Accuracy delta:** `+0.0034`
- **Macro-F1 delta:** `+0.0135`

### Weighted BERT vs RoBERTa
- **Accuracy delta:** `-0.0100`
- **Macro-F1 delta:** `+0.0042`

These results show that **RoBERTa currently has slightly higher test accuracy**, but **weighted BERT achieves better Macro-F1** and more balanced class performance.

## Additional model notes

### TF-IDF + Logistic Regression
The TF-IDF baseline remains the main traditional baseline for the project.

Final result:
- **Accuracy:** `0.6235`
- **Macro-F1:** `0.6005`

### Unweighted BERT
The unweighted BERT baseline was evaluated across 3 random seeds.

Mean result:
- **Test Accuracy:** `0.6369 ± 0.0028`
- **Test Macro-F1:** `0.6169 ± 0.0054`

This model consistently outperformed TF-IDF, but still showed weaker recall on the **FAKE** class.

### RoBERTa
RoBERTa was run once under the same overall LIAR binary setup.

Result:
- **Best epoch:** `3`
- **Validation Accuracy:** `0.6558`
- **Validation Macro-F1:** `0.6435`
- **Test Accuracy:** `0.6504`
- **Test Macro-F1:** `0.6262`

RoBERTa currently gives the highest single-run accuracy, but it does not outperform weighted BERT on Macro-F1.

## Main interpretation
The current baseline results suggest three main conclusions.

First, transformer-based baselines consistently outperform the TF-IDF baseline on LIAR binary fake news detection.

Second, the improvement from TF-IDF to BERT is **stable but moderate**, rather than dramatic. This suggests that contextual transformer representations help, but do not fully solve the difficulty of the task.

Third, adding **class-weighted loss** is an effective improvement. It reduces the model’s bias toward the **REAL** class, improves balance between the two classes, and produces the strongest overall Macro-F1 result among the tested baselines.

## Class balance observation
A central challenge in this task is that models tend to achieve stronger recall on **REAL** than on **FAKE**.

The weighted BERT result reduces this imbalance and gives the strongest overall balance among the tested baselines. This is one of the main reasons it is treated as the current best model.

## Model status
Current status of the main baselines:

- **TF-IDF + Logistic Regression:** completed
- **BERT-base:** completed, 3-seed stability confirmed
- **BERT-base + weighted loss:** completed, 3-seed stability confirmed
- **RoBERTa-base:** completed as a single run

## Current conclusion
At the current stage of the project, **weighted BERT** is the strongest main baseline overall.

RoBERTa is still important as a comparison model because it gives higher test accuracy, but weighted BERT is currently the more suitable primary model because it achieves the best average Macro-F1 and better class balance.

## Next priorities
The next project priorities are no longer simple linear-model comparisons.

The main next steps are:

1. **error analysis** of the weighted BERT model,
2. **literature review expansion**,
3. **cross-dataset / cross-domain pipeline design and implementation**.

## Notes
- TF-IDF remains the main sparse baseline.
- Weighted BERT is currently the main neural baseline.
- RoBERTa should not yet be treated as the final best model, because it has only been run once and currently trades slightly higher accuracy for weaker class balance.
