# Supervisor Meeting Talking Points - 2026-05-29

## 30-second summary

This week I finished the cross-dataset stage. The direct LIAR-to-FakeNewsNet result is poor, but that failure is now useful because the intermediate fine-tuning experiment shows how it can be recovered. So the dissertation story is no longer only "the model does not transfer"; it is "direct transfer is unreliable, and target-domain adaptation is needed."

## What I did this week

1. Completed strict LIAR-to-FakeNewsNet transfer evaluation.
2. Added an unweighted BERT transfer control.
3. Ran intermediate fine-tuning on 5%, 10%, and 20% FakeNewsNet target-domain training data.
4. Added a small TELLER-like reasoning-atoms pilot.
5. Updated Chapter 6, Discussion, Conclusion, and the final Word/PDF draft.
6. Repaired layout issues in figures, tables, page breaks, and static contents/list pages.

## How to explain the direct-transfer failure

The direct transfer experiment trains on LIAR statements and tests directly on FakeNewsNet titles. This is intentionally strict. Under this setting, the LIAR-trained weighted RoBERTa model does not generalise well: it predicts FAKE for almost everything in the FakeNewsNet target set.

The key point is that this is not just an accuracy drop. The class-level recalls show the failure mode:

- REAL recall becomes very low.
- FAKE recall becomes very high.
- Macro-F1 drops because the model loses class balance.

This supports the dataset-shift argument.

## How to explain intermediate fine-tuning

I then tested whether adding a small amount of labelled target-domain FakeNewsNet training data helps.

The result is:

- 5% target data is not enough and flips the model toward REAL.
- 10% target data gives the first effective recovery.
- 20% target data gives the best current result.

So the useful conclusion is not that the model is simply bad. The conclusion is that direct transfer is unreliable, but target-domain adaptation can recover performance.

## How to explain TELLER-like atoms

I should be careful here.

I did not reproduce TELLER. I only tested a simplified TELLER-like idea: generate reasoning-atom features and train a simple classifier on them.

The pilot suggests:

- atom features contain some signal,
- but they do not solve cross-dataset bias by themselves,
- so they should remain supporting analysis.

## Questions to ask the supervisor

1. Is the current thesis framing acceptable?
2. Do I need more seeds for the 10% and 20% intermediate fine-tuning settings?
3. Should the TELLER-like pilot be in the main chapter or appendix?
4. Is the current dissertation draft close enough for final polishing, or should I focus on one chapter first?

## Files to point to

- `thesis_writeup/dissertation_final.pdf`
- `results/integrated_experiment_summary/integrated_main_results_table.md`
- `results/intermediate_finetuning/intermediate_finetuning_weighted_roberta_seeds_42.md`
- `results/cross_dataset/cross_dataset_model_comparison.md`
