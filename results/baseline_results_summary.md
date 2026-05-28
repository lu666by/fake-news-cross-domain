# LIAR Baseline Results Summary

## Task
This file summarises the current **in-domain binary fake news detection baselines** on the **LIAR** dataset.

Binary label mapping used in this project:

- **REAL (0):** `true`, `mostly-true`, `half-true`
- **FAKE (1):** `barely-true`, `false`, `pants-fire`

All current baseline experiments use **statement** as the main input text unless explicitly stated otherwise.

## Main results

| Model | Accuracy | Macro-F1 | Notes |
|---|---:|---:|---|
| TF-IDF + Logistic Regression | 0.6235 | 0.6005 | Final sparse baseline; effectively deterministic |
| BERT-base (5-run mean) | 0.6425 ± 0.0095 | 0.6231 ± 0.0122 | Main unweighted neural baseline |
| BERT-base + weighted loss (5-run mean) | 0.6412 ± 0.0065 | 0.6322 ± 0.0090 | Stronger FAKE recall |
| RoBERTa-base + weighted loss (5-run mean) | 0.6522 ± 0.0074 | 0.6396 ± 0.0080 | Current strongest overall model |

## Class-wise recall summary

| Model | REAL Recall | FAKE Recall |
|---|---:|---:|
| TF-IDF + Logistic Regression | 0.7661 | 0.4394 |
| BERT-base (5-run mean) | N/A | N/A |
| BERT-base + weighted loss (5-run mean) | 0.7048 ± 0.0292 | 0.5591 ± 0.0447 |
| RoBERTa-base + weighted loss (5-run mean) | 0.7443 ± 0.0153 | 0.5335 ± 0.0199 |

## Current main model
The current **main overall model** is **RoBERTa-base + weighted loss**.

It is preferred because it gives the strongest overall test performance, with the highest mean accuracy and the highest mean macro-F1 among the tested baselines.

At the same time, **weighted BERT** remains an important comparison model because it gives stronger **FAKE recall**.

## Main interpretation
The current results show that transformer baselines consistently outperform the sparse TF-IDF baseline on LIAR binary classification.

The improvement is meaningful but moderate rather than dramatic. This suggests that the LIAR task remains difficult even with stronger transformer models, especially because the statements are short and the binary label boundary is narrow.

A second important conclusion is that **class balance remains a central issue**. Weighted training is helpful, but different weighted models optimise different strengths:

- **weighted BERT** is stronger on **FAKE recall**
- **weighted RoBERTa** is stronger on **overall performance**

## Current conclusion
At the current stage of the project:

- **TF-IDF + Logistic Regression** remains the main sparse baseline,
- **BERT-base** remains the main unweighted neural baseline,
- **weighted BERT** is the key comparison model for FAKE-recall and class-balance analysis,
- **weighted RoBERTa** is the current strongest overall model.
