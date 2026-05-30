# Progress Summary (living document)

> Note for supervisor: `tracking.md` is the evidence index. This file is the short narrative progress update.

## Latest update: 2026-05-30

## What I did after the 2026-05-29 supervisor meeting

I completed the supervisor-requested reliability checks for the main comparable rows and prepared a supervisor-facing reading package.

### 1. Re-ran titles-only direct transfer with five seeds

The held-out titles-only direct transfer baseline is now a five-seed result rather than a seed-42-only observation.

| Setting | Evidence | Accuracy | Macro-F1 | REAL recall | FAKE recall |
|---|---|---:|---:|---:|---:|
| LIAR -> held-out FakeNewsNet title test | 5 seeds | 0.2725 | 0.2364 | 0.0377 | 0.9842 |

Interpretation: titles-only direct transfer remains consistently weak and strongly FAKE-biased. The old seed-42 result was not a lucky or unlucky exception.

Evidence:

- `results/intermediate_finetuning/titles_only_direct_transfer_heldout_5seed_summary_20260530.md`
- `results/integrated_experiment_summary/integrated_main_results_table.md`

### 2. Re-ran 10% and 20% intermediate fine-tuning with five seeds

| Setting | Evidence | Accuracy | Macro-F1 | REAL recall | FAKE recall |
|---|---|---:|---:|---:|---:|
| LIAR -> 10% FNN -> FNN test | 5 seeds | 0.8083 | 0.7035 | 0.9305 | 0.4379 |
| LIAR -> 20% FNN -> FNN test | 5 seeds | 0.8243 | 0.7463 | 0.9167 | 0.5444 |

Interpretation: 10% is the more data-efficient stable recovery point. 20% is currently the strongest absolute target-fraction result. The 20% row is no longer seed-42 only.

Evidence:

- `results/intermediate_finetuning/intermediate_ft_10pct_5seed_summary_20260530.md`
- `results/intermediate_finetuning/intermediate_ft_20pct_5seed_summary_20260530.md`

### 3. Added dataset-shift explanation material

I added LIAR vs FakeNewsNet descriptive analysis for length, vocabulary overlap, and distinctive terms. This supports the thesis explanation for why strict cross-dataset transfer is difficult.

Evidence:

- `results/dataset_shift_analysis/liar_vs_fakenewsnet_explanation_20260530.md`
- `results/dataset_shift_analysis/vocabulary_overlap.md`
- `results/dataset_shift_analysis/dataset_distinctive_terms.md`

### 4. Tightened the LLM atom pilot wording

The TELLER-like atom experiment is now described only as a current-setup pilot. The safe wording is: the current DeepSeek V4 Flash reasoning-atom setup shows limited performance in this pilot.

Evidence:

- `results/llm_reasoning_atoms/pilot_positioning_note_20260530.md`
- `results/llm_reasoning_atoms/max_per_group_100_summary.md`

### 5. Prepared supervisor-facing materials

The recommended supervisor package is Chapter 2/3 plus the compact updated result summary. Chapter 6 remains an internal note until the supervisor decides how strongly to frame 10% vs 20%.

Evidence:

- `thesis_writeup/supervisor_materials_20260530/supervisor_ch2_ch3_results_2026-05-30.pdf`
- `thesis_writeup/supervisor_materials_20260530/meeting_outline_2026-05-30.pdf`
- `thesis_writeup/supervisor_materials_20260530/chapter6_internal_rerun_update_2026-05-30.md`

## Current supervisor-facing story

> Strict LIAR-to-FakeNewsNet title transfer is consistently weak across seeds. Small target-domain intermediate fine-tuning recovers performance: 10% is the more data-efficient stable setting, while 20% is the strongest absolute five-seed result. The LLM atom experiment is only a current-setup pilot with limited performance, not a main empirical claim.

## What I want to discuss with the supervisor next

1. Whether to frame the main adaptation claim around 10% efficiency, 20% best absolute performance, or both.
2. Whether the 1000-row atom pilot should remain in Chapter 6, move to appendix, or be expanded with additional samples.
3. Whether Chapter 2/3 are clear enough for the next full draft review.

---

## Previous update: 2026-05-29

## What I did this week

This week I moved the project from "strict cross-dataset transfer fails" to a stronger and more useful dissertation story: direct transfer is unreliable, but intermediate target-domain fine-tuning can recover performance in the current experimental pass.

### 1. Completed the strict cross-dataset evaluation

I evaluated LIAR-trained baselines on FakeNewsNet minimal titles.

Main finding:

- Weighted RoBERTa performs best in-domain on LIAR, but under strict LIAR-to-FakeNewsNet transfer it becomes strongly FAKE-biased.
- On FakeNewsNet combined titles, weighted RoBERTa reaches Macro-F1 `0.2358`, with REAL recall only `0.0372` and FAKE recall `0.9827`.
- The unweighted BERT control shows a similar transfer failure, so the problem appears to be mainly dataset shift rather than only the class-weighted loss.

Evidence:

- `results/cross_dataset/cross_dataset_model_comparison.md`
- `results/cross_dataset/unweighted_bert_results_analysis.md`

### 2. Added intermediate target-domain fine-tuning

Following the supervisor's previous direction, I tested whether a small amount of FakeNewsNet target-domain training data can recover the direct-transfer failure.

Main seed-42 result:

| Setting | Accuracy | Macro-F1 | REAL recall | FAKE recall |
|---|---:|---:|---:|---:|
| Direct LIAR -> FNN test | 0.2601 | 0.2178 | 0.0183 | 0.9930 |
| LIAR -> 5% FNN -> FNN test | 0.7519 | 0.4292 | 1.0000 | 0.0000 |
| LIAR -> 10% FNN -> FNN test | 0.8125 | 0.7141 | 0.9304 | 0.4553 |
| LIAR -> 20% FNN -> FNN test | 0.8231 | 0.7447 | 0.9157 | 0.5421 |

Interpretation:

- 5% target fine-tuning is not enough and flips into an all-REAL-like model.
- 10% becomes the first effective adaptation point.
- This 2026-05-29 note has been superseded by the 2026-05-30 five-seed reruns; 20% is now the strongest absolute five-seed result.

Evidence:

- `notebooks/13_intermediate_finetuning_fakenewsnet.py`
- `results/intermediate_finetuning/intermediate_finetuning_weighted_roberta_seeds_42.md`
- `results/integrated_experiment_summary/integrated_main_results_table.md`

### 3. Added a small TELLER-like reasoning-atoms pilot

I implemented an exploratory reasoning-atoms experiment inspired by TELLER, using generated atom-style features followed by a simple classifier.

Main conclusion:

- The atoms carry some signal, especially in-domain.
- They do not remove the cross-dataset bias by themselves.
- I should present this only as supporting analysis, not as full TELLER reproduction or a main contribution.

Evidence:

- `notebooks/12_llm_reasoning_atoms_teller_like.py`
- `results/llm_reasoning_atoms/max_per_group_100_summary.md`

### 4. Updated the dissertation draft and repaired presentation issues

The current dissertation draft has been updated with:

- intermediate fine-tuning results,
- integrated Chapter 6 interpretation,
- revised Discussion and Conclusion,
- repaired tables and figures,
- static table-of-contents/list-of-figures/list-of-tables page numbers,
- final Word/PDF layout export.

Evidence:

- `thesis_writeup/dissertation_final.docx`
- `thesis_writeup/dissertation_final.pdf`

## Main thesis story now

The strongest explanation is:

> A LIAR-trained fake-news classifier can look acceptable in-domain but fail sharply when transferred to FakeNewsNet titles. The failure is not just caused by class weighting; it reflects dataset shift. The current intermediate target-domain fine-tuning pass shows that the failure can be recovered when some labelled target data is available, so the practical conclusion is not "the model is useless" but "direct transfer is unreliable without adaptation."

## What I want to discuss with the supervisor

1. Whether the intermediate fine-tuning result is strong enough as the main recovery experiment.
2. Whether I should repeat the 10% and 20% target fine-tuning settings over multiple seeds.
3. Whether the TELLER-like pilot should remain in the main text or move partly to appendix.
4. Whether the current dissertation framing is acceptable for final write-up.

---

## Previous update: 2026-05-10

Earlier progress focused on TELLER feasibility, the MSc literature review standard, and expansion of the literature review draft. Those outputs remain in `papers/`, `results/teller_feasibility_note.md`, and `thesis_writeup/literature_review_*`.
