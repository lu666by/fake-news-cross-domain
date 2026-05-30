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

The project is now in the thesis-consolidation and supervisor-review stage. The 2026-05-29 supervisor-requested reruns have been completed for the main comparable rows.

Completed work:

- Built local TF-IDF, BERT, weighted BERT, RoBERTa, and weighted RoBERTa baselines.
- Stabilised the main LIAR transformer comparison with five-seed results.
- Ran strict LIAR-to-FakeNewsNet title transfer experiments.
- Added an unweighted BERT transfer control to check whether class weighting alone explains the transfer failure.
- Re-ran the held-out titles-only direct transfer baseline with five seeds.
- Re-ran 10% and 20% intermediate fine-tuning with the same five seeds.
- Added LIAR vs FakeNewsNet dataset-shift analysis for title length, vocabulary overlap, and distinctive terms.
- Kept the exploratory TELLER-like LLM reasoning-atoms pilot as current-setup evidence only.
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

The intermediate target-domain fine-tuning reruns change the interpretation of the cross-dataset experiment. Direct transfer is consistently weak, but target-domain fine-tuning recovers performance when a small labelled target subset is available.

| Setting | Evidence | Accuracy | Macro-F1 | REAL recall | FAKE recall | Interpretation |
|---|---|---:|---:|---:|---:|---|
| LIAR -> held-out FNN title test | 5 seeds | 0.2725 | 0.2364 | 0.0377 | 0.9842 | Direct transfer is consistently FAKE-biased |
| LIAR -> 5% FNN -> FNN test | seed 42 | 0.7519 | 0.4292 | 1.0000 | 0.0000 | High accuracy is misleading; model collapses to REAL |
| LIAR -> 10% FNN -> FNN test | 5 seeds | 0.8083 | 0.7035 | 0.9305 | 0.4379 | Stable, data-efficient recovery |
| LIAR -> 20% FNN -> FNN test | 5 seeds | 0.8243 | 0.7463 | 0.9167 | 0.5444 | Best absolute target-fraction result so far |

Interpretation:

- Direct transfer alone is not reliable.
- Small target supervision can be unstable.
- The 10% setting is the more data-efficient stable recovery point.
- The 20% setting is currently the strongest absolute five-seed result.

### 4. TELLER-like pilot

The TELLER-like LLM reasoning-atoms experiment is included only as an exploratory pilot.

Main interpretation:

- Coarse LLM-generated atoms can carry some signal.
- They do not remove the cross-dataset bias problem by themselves.
- The current DeepSeek V4 Flash reasoning-atom setup shows limited performance in this pilot.
- The dissertation should not claim full TELLER reproduction; it should only report what this current setup did in this pilot.

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
