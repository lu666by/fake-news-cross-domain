# Results

This folder stores the main result summaries and compact evidence files for the dissertation.

## Key files for supervisor review

- `integrated_experiment_summary/integrated_main_results_table.md`
  One-table view of in-domain, direct transfer, intermediate fine-tuning, and TELLER-like pilot results.

- `integrated_experiment_summary/experiment_credibility_audit.md`
  Checks that target-domain fine-tuning does not leak test data and that metrics are traceable.

- `cross_dataset/cross_dataset_model_comparison.md`
  Direct LIAR-to-FakeNewsNet transfer comparison.

- `intermediate_finetuning/intermediate_finetuning_weighted_roberta_seeds_42.md`
  Intermediate fine-tuning result for weighted RoBERTa, seed 42.

- `intermediate_finetuning/intermediate_ft_10pct_5seed_summary_20260530.md`
  Five-seed summary for 10% intermediate fine-tuning.

- `intermediate_finetuning/intermediate_ft_20pct_5seed_summary_20260530.md`
  Five-seed summary for 20% intermediate fine-tuning.

- `dataset_shift_analysis/liar_vs_fakenewsnet_explanation_20260530.md`
  Dataset-shift explanation using length, vocabulary overlap, and distinctive-term analysis.

- `llm_reasoning_atoms/max_per_group_100_summary.md`
  TELLER-like reasoning-atoms pilot summary.

## Main current reading

1. LIAR in-domain transformer baselines are reasonable but modest.
2. Strict LIAR-to-FakeNewsNet transfer fails through severe target-domain class bias.
3. Intermediate fine-tuning with 10-20% target-domain training data recovers performance in the current five-seed reruns.
4. TELLER-like atoms are useful as a small supporting pilot, not a main contribution.

## Caution for thesis wording

- Treat the 10% row as the more data-efficient stable recovery point.
- Treat the 20% row as the strongest absolute five-seed target-fraction result so far, not as a final optimised target-data percentage.
- Keep the TELLER-like atom pilot limited to the current DeepSeek V4 Flash reasoning-atom setup.

## What is intentionally not stored here

- Raw datasets.
- Model checkpoints.
- Full local render/QA caches.

These are kept outside GitHub to avoid unnecessary size and privacy/copyright issues.
