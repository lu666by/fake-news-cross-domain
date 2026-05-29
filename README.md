# MSc Project - Cross-dataset Generalisation for Fake News Detection

**Supervisor:** Dr. Josephine Griffith
**Student:** Boyu Lu
**Current thesis title:** Cross-Dataset Generalisation for Fake News Detection Using Reproducible Transformer-Based Baselines

---

## Project overview

This project studies whether fake-news detection models that work on one dataset remain reliable when they are applied to another dataset with different text style, label distribution, and annotation assumptions.

The dissertation is not framed as a new model architecture. Its main contribution is a careful, reproducible, and class-sensitive evaluation of practical baselines:

- LIAR in-domain binary fake-news classification.
- LIAR-to-FakeNewsNet strict transfer.
- Class-level recall analysis, especially FAKE recall.
- Intermediate target-domain fine-tuning as a recovery strategy.
- A small TELLER-like reasoning-atoms pilot as supporting analysis, not the main contribution.

---

## Current project stage

The project is now in the thesis-consolidation and supervisor-review stage.

Completed work:

- Built local TF-IDF, BERT, weighted BERT, RoBERTa, and weighted RoBERTa baselines.
- Stabilised the main LIAR transformer comparison with five-seed results.
- Ran strict LIAR-to-FakeNewsNet title transfer experiments.
- Added an unweighted BERT transfer control to check whether class weighting alone explains the transfer failure.
- Ran the current intermediate fine-tuning pass using 5%, 10%, and 20% of target-domain FakeNewsNet training data.
- Added an exploratory TELLER-like LLM reasoning-atoms pilot.
- Updated and visually QA-checked the dissertation draft in `thesis_writeup/dissertation_final.docx` and `thesis_writeup/dissertation_final.pdf`.

---

## Current task setting

### Source dataset

- **LIAR**
- Input text: `statement`
- Binary mapping:
  - **REAL (0):** `true`, `mostly-true`, `half-true`
  - **FAKE (1):** `barely-true`, `false`, `pants-fire`

### Target dataset

- **FakeNewsNet minimal title dataset**
- Input text: news title only
- Main strict-transfer setting: train on LIAR, test directly on FakeNewsNet titles
- Main adaptation setting: train on LIAR, then intermediate fine-tune on 5%, 10%, or 20% of FakeNewsNet training titles, then evaluate on the held-out FakeNewsNet test split

### Evaluation emphasis

- Accuracy is reported, but it is not sufficient by itself.
- Macro-F1 and class-level REAL/FAKE recall are treated as the main evidence for transfer failure and recovery.
- Intermediate fine-tuning rows are currently seed-42 results unless otherwise stated.

---

## Current main findings

### 1. LIAR in-domain baseline

| Model | Accuracy | Macro-F1 | REAL recall | FAKE recall | Notes |
|---|---:|---:|---:|---:|---|
| TF-IDF + Logistic Regression | 0.6235 | 0.6005 | 0.7661 | 0.4394 | Deterministic sparse baseline |
| Weighted RoBERTa | 0.6522 | 0.6396 | 0.7443 | 0.5335 | Best current in-domain local baseline |
| Weighted BERT | 0.6412 | 0.6322 | 0.7048 | 0.5591 | Stronger FAKE recall |

Interpretation:

- Weighted RoBERTa is the strongest overall LIAR baseline.
- Weighted BERT remains useful because it gives higher FAKE recall.
- Accuracy alone is not enough; Macro-F1 and class-level recall are needed.

### 2. Strict LIAR-to-FakeNewsNet transfer

The LIAR-trained transformer models fail badly under strict direct transfer to FakeNewsNet titles.

Key result:

- Weighted RoBERTa direct transfer to FakeNewsNet combined titles: Macro-F1 `0.2358`, REAL recall `0.0372`, FAKE recall `0.9827`.

Interpretation:

- The transfer failure is not a small performance drop.
- The model becomes strongly biased toward FAKE on the target dataset.
- The unweighted BERT control shows that this is mainly a dataset-shift problem, not only a class-weighting artifact.

### 3. Intermediate fine-tuning recovery

The current seed-42 intermediate target-domain fine-tuning pass changes the interpretation of the cross-dataset experiment.

| Setting | Accuracy | Macro-F1 | REAL recall | FAKE recall | Interpretation |
|---|---:|---:|---:|---:|---|
| LIAR -> held-out FNN test | 0.2601 | 0.2178 | 0.0183 | 0.9930 | Direct transfer collapses toward FAKE |
| LIAR -> 5% FNN -> FNN test | 0.7519 | 0.4292 | 1.0000 | 0.0000 | Flips into an all-REAL-like model |
| LIAR -> 10% FNN -> FNN test | 0.8125 | 0.7141 | 0.9304 | 0.4553 | First effective adaptation point |
| LIAR -> 20% FNN -> FNN test | 0.8231 | 0.7447 | 0.9157 | 0.5421 | Best current seed-42 target-domain result |

Interpretation:

- Direct transfer alone is not reliable.
- Small target supervision can be unstable.
- Around 10-20% target-domain fine-tuning gives a clear recovery signal in the current pass.
- The next reliability check is to repeat the 10% and 20% settings across more seeds if the supervisor wants a stronger experimental claim.

### 4. TELLER-like pilot

The TELLER-like LLM reasoning-atoms experiment is included only as an exploratory pilot.

Main interpretation:

- Coarse LLM-generated atoms can carry some signal.
- They do not remove the cross-dataset bias problem by themselves.
- The dissertation should not claim full TELLER reproduction.

---

## Repository structure

- `tracking.md`
  Main task tracker and evidence index.

- `progress/progress_summary.md`
  Narrative weekly progress update.

- `progress/supervisor_update_2026-05-29.md`
  Short message that can be sent to the supervisor before the next meeting.

- `progress/supervisor_meeting_talking_points_2026-05-29.md`
  Speaking notes for explaining this week's work in the meeting.

- `plans/plan_next_2_weeks.md`
  Current forward plan after the latest results.

- `notebooks/`
  Main experiment notebooks and scripts.

- `results/`
  Result summaries, CSV outputs, figures, and interpretation notes.

- `papers/`
  Reading list and selected paper summaries. PDF files are not stored in this repository.

- `thesis_writeup/`
  Current dissertation draft and PDF export.

---

## Recommended files before the next supervisor meeting

Use the text in the first file as the email body, and attach or link the other two:

1. `progress/supervisor_update_2026-05-29.md`
2. `thesis_writeup/dissertation_final.pdf`
3. `results/integrated_experiment_summary/integrated_main_results_table.md`

Optional if the supervisor wants more detail:

- `results/integrated_experiment_summary/experiment_credibility_audit.md`
- `results/cross_dataset/cross_dataset_model_comparison.md`
- `results/intermediate_finetuning/intermediate_finetuning_weighted_roberta_seeds_42.md`

---

## Short explanation for the supervisor

This week I moved the project from a direct-transfer failure result into a clearer dissertation contribution. The original strict LIAR-to-FakeNewsNet transfer result was poor, but the current intermediate fine-tuning experiment shows that the failure can be recovered when a small amount of target-domain supervision is available. This gives the thesis a stronger conclusion: the issue is not simply that the model is useless, but that direct transfer is unreliable and target-domain adaptation is needed.

The dissertation draft has also been updated and visually checked so it is now in a supervisor-readable state.

---

## Implementation references

Some implementation ideas were informed by publicly available repositories related to fake news detection and the LIAR dataset:

- `https://github.com/tomtuamnuq/LIAR-Detect-Fake-News-Statement-Classification`
- `https://github.com/moscatena/Fake-News-Classification`

These repositories were used only as implementation references. They do not replace the notebooks and scripts in this repository. The files here remain project-specific working versions written for this dissertation workflow.
