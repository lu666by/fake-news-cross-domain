# LLM-Generated Reasoning Atoms Pilot (`max_per_group=100`)

- Date: 2026-05-25
- LLM: DeepSeek V4 Flash
- Cached atom rows: 1,000
- Sampling: balanced 100 rows per dataset/split/label group
- Atom features: `emotional_language`, `exaggerated_claim`, `specific_evidence`, `source_reference`, `logical_consistency`, `clickbait_style`
- Decision models: Logistic Regression and Random Forest
- Fixed positioning: exploratory TELLER-like pilot only; not a main contribution.

## Logistic Regression

| Experiment | Train n | Test n | Accuracy | Macro-F1 | REAL Recall | FAKE Recall | Confusion Matrix |
|---|---:|---:|---:|---:|---:|---:|---|
| LIAR atoms -> LIAR | 400 | 200 | 0.6200 | 0.6198 | 0.6000 | 0.6400 | `[[60, 40], [36, 64]]` |
| LIAR atoms -> FakeNewsNet | 400 | 200 | 0.5300 | 0.4405 | 0.1300 | 0.9300 | `[[13, 87], [7, 93]]` |
| FakeNewsNet atoms -> FakeNewsNet | 200 | 200 | 0.6000 | 0.6000 | 0.5900 | 0.6100 | `[[59, 41], [39, 61]]` |

## Random Forest

| Experiment | Train n | Test n | Accuracy | Macro-F1 | REAL Recall | FAKE Recall | Confusion Matrix |
|---|---:|---:|---:|---:|---:|---:|---|
| LIAR atoms -> LIAR | 400 | 200 | 0.6050 | 0.6049 | 0.6200 | 0.5900 | `[[62, 38], [41, 59]]` |
| LIAR atoms -> FakeNewsNet | 400 | 200 | 0.5300 | 0.4686 | 0.1900 | 0.8700 | `[[19, 81], [13, 87]]` |
| FakeNewsNet atoms -> FakeNewsNet | 200 | 200 | 0.6000 | 0.5998 | 0.5800 | 0.6200 | `[[58, 42], [38, 62]]` |

## Initial Reading

- The in-domain LIAR setting reaches about 0.61-0.62 Macro-F1, showing that the LLM-generated atoms contain some usable signal.
- The LIAR -> FakeNewsNet transfer setting drops sharply in Macro-F1, especially for Logistic Regression.
- Both decision models heavily over-predict FAKE in the cross-dataset setting: FAKE recall is high, but REAL recall is very low.
- FakeNewsNet in-domain performance is around 0.60 Macro-F1, suggesting that target-domain atoms can support a weak but meaningful decision model.
- This supports the dissertation argument that TELLER-like reasoning signals do not automatically solve cross-dataset generalisation; domain and style shift still matter.

## Dissertation Positioning

Treat this experiment as an exploratory pilot inspired by TELLER's separation between cognition-style signal generation and decision aggregation. It should not be framed as a reproduced TELLER system or as the dissertation's main contribution. Its role is to provide a small supporting analysis showing that LLM-generated reasoning atoms contain some signal but remain vulnerable to cross-dataset shift and decision bias.
