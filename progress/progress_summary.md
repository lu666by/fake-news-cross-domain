# Progress Summary (living document)

> Note for supervisor: `tracking.md` is the evidence index. This file is the short narrative progress update.

## Latest update: 2026-05-29

## What I did this week

This week I moved the project from "strict cross-dataset transfer fails" to a stronger and more useful dissertation story: direct transfer is unreliable, but intermediate target-domain fine-tuning can recover performance.

### 1. Completed the strict cross-dataset evaluation

I evaluated LIAR-trained baselines on FakeNewsNet minimal titles.

Main finding:

- Weighted RoBERTa performs best in-domain on LIAR, but under strict LIAR-to-FakeNewsNet transfer it becomes strongly FAKE-biased.
- On FakeNewsNet combined titles, weighted RoBERTa reaches Macro-F1 `0.2358`, with REAL recall only `0.0372` and FAKE recall `0.9827`.
- The unweighted BERT control shows a similar transfer failure, so the problem is mainly dataset shift rather than only the class-weighted loss.

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
- 20% is the best current result and gives a much stronger conclusion than direct transfer alone.

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

> A LIAR-trained fake-news classifier can look acceptable in-domain but fail sharply when transferred to FakeNewsNet titles. The failure is not just caused by class weighting; it reflects dataset shift. Intermediate target-domain fine-tuning shows that the failure can be recovered when some labelled target data is available, so the practical conclusion is not "the model is useless" but "direct transfer is unreliable without adaptation."

## What I want to discuss with the supervisor

1. Whether the intermediate fine-tuning result is strong enough as the main recovery experiment.
2. Whether I should repeat the 10% and 20% target fine-tuning settings over multiple seeds.
3. Whether the TELLER-like pilot should remain in the main text or move partly to appendix.
4. Whether the current dissertation framing is acceptable for final write-up.

---

## Previous update: 2026-05-10

Earlier progress focused on TELLER feasibility, the MSc literature review standard, and expansion of the literature review draft. Those outputs remain in `papers/`, `results/teller_feasibility_note.md`, and `thesis_writeup/literature_review_*`.
