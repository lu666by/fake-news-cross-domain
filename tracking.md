# Plan + Progress Tracker

This file keeps the original branch format: one compact tracker with task status and evidence paths.

| Task | Start | Due | Steps (short) | Status | Evidence (path/link) |
|---|---:|---:|---|---|---|
| LIAR: load + inspect dataset | 2026-03-05 | 2026-03-18 | Load train/valid/test splits; inspect label counts and binary mapping | Completed | `notebooks/01_liar_load.ipynb` |
| LIAR: TF-IDF baseline | 2026-03-08 | 2026-03-25 | Run TF-IDF + Logistic Regression; report Accuracy, Macro-F1, confusion matrix | Completed | `notebooks/02_tfidf_baseline.ipynb`; `results/liar_baseline.md` |
| LIAR: TF-IDF determinism check | 2026-04-12 | 2026-04-12 | Verify repeated-seed stability for deterministic sparse baseline | Completed | `results/tfidf_seed_determinism_check.md`; `results/tfidf_seed_determinism_check.csv` |
| LIAR: BERT baseline | 2026-04-08 | 2026-04-12 | Run unweighted BERT and 5-seed stability check | Completed | `notebooks/03_bert_baseline.ipynb`; `results/bert_seed_sweep_results.md` |
| LIAR: weighted BERT baseline | 2026-04-08 | 2026-04-12 | Add train-split class-weighted loss; run 5 seeds | Completed | `notebooks/04_bert_weighted_baseline.ipynb`; `results/bert_weighted_seed_sweep_results.md` |
| LIAR: RoBERTa baseline | 2026-04-08 | 2026-04-12 | Run unweighted RoBERTa under same LIAR setup | Completed | `notebooks/05_roberta_baseline.ipynb`; `results/liar_roberta_baseline_run_output.md` |
| LIAR: weighted RoBERTa baseline | 2026-04-10 | 2026-04-12 | Run weighted RoBERTa and compare with BERT variants | Completed | `notebooks/06_roberta_weighted_baseline.ipynb`; `results/roberta_weighted_seed_sweep_results.md` |
| LIAR: context comparison | 2026-04-12 | 2026-04-12 | Compare statement-only vs statement+context for weighted RoBERTa | Completed | `notebooks/07_roberta_weighted_context_comparison.py`; `results/roberta_weighted_statement_vs_context_comparison.md` |
| LIAR: threshold tuning | 2026-04-12 | 2026-04-12 | Scan validation thresholds for weighted RoBERTa | Completed | `notebooks/08_roberta_weighted_threshold_tuning.py`; `results/roberta_weighted_threshold_tuning_seed52.md` |
| LIAR: error analysis | 2026-04-12 | 2026-04-12 | Analyse weighted BERT vs weighted RoBERTa error patterns | Completed | `results/liar_error_analysis_weighted_roberta_vs_weighted_bert.md` |
| TELLER feasibility investigation | 2026-05-05 | 2026-05-10 | Read TELLER paper/repo; assess reproducibility and API dependency | Completed | `papers/summaries/liu2024_teller.md`; `results/teller_feasibility_note.md` |
| Literature review expansion | 2026-05-08 | 2026-05-21 | Add datasets, transformer, LLM/reasoning, imbalance, robustness, and gap sections | Completed | `thesis_writeup/literature_review_draft_en.md`; `papers/reading_list.md` |
| FakeNewsNet minimal target dataset preparation | 2026-05-11 | 2026-05-11 | Prepare title-only target dataset note and inspection outputs | Completed | `results/data_inspection/fakenewsnet_minimal_inspection.md` |
| Cross-dataset TF-IDF transfer | 2026-05-11 | 2026-05-14 | Train on LIAR and test on FakeNewsNet titles | Completed | `notebooks/09_cross_dataset_tfidf_liar_to_fakenewsnet.py`; `results/cross_dataset/cross_dataset_tfidf_liar_to_fakenewsnet.md` |
| Cross-dataset transformer transfer | 2026-05-14 | 2026-05-21 | Run weighted BERT/RoBERTa and unweighted BERT transfer comparison | Completed | `notebooks/10_cross_dataset_transformer_liar_to_fakenewsnet.py`; `results/cross_dataset/cross_dataset_model_comparison.md` |
| Cross-dataset result summaries and figures | 2026-05-12 | 2026-05-21 | Generate tables and visual summaries for Chapter 6 | Completed | `notebooks/11_cross_dataset_results_summary_figures.py`; `results/cross_dataset/figures/` |
| TELLER-like reasoning-atoms pilot | 2026-05-24 | 2026-05-25 | Generate atom-style features and evaluate simple classifiers | Completed | `notebooks/12_llm_reasoning_atoms_teller_like.py`; `results/llm_reasoning_atoms/max_per_group_100_summary.md` |
| Intermediate FakeNewsNet fine-tuning | 2026-05-25 | 2026-05-25 | Fine-tune weighted RoBERTa with 5%, 10%, 20% target-domain training data | Completed | `notebooks/13_intermediate_finetuning_fakenewsnet.py`; `results/intermediate_finetuning/intermediate_finetuning_weighted_roberta_seeds_42.md` |
| Integrated experiment summary | 2026-05-25 | 2026-05-25 | Combine in-domain, direct transfer, intermediate fine-tuning, and TELLER-like rows | Completed | `results/integrated_experiment_summary/integrated_main_results_table.md` |
| Experiment credibility audit | 2026-05-25 | 2026-05-25 | Check metric traceability and train/test separation | Completed | `results/integrated_experiment_summary/experiment_credibility_audit.md`; `results/integrated_experiment_summary/manuscript_consistency_check.md` |
| Dissertation draft update | 2026-05-25 | 2026-05-28 | Update Chapter 6, Discussion, Conclusion, figures, tables, and layout | Completed | `thesis_writeup/dissertation_final.docx`; `thesis_writeup/dissertation_final.pdf` |
| Supervisor meeting preparation | 2026-05-29 | 2026-05-29 | Prepare pre-meeting update and talking points | Completed | `progress/supervisor_update_2026-05-29.md`; `progress/supervisor_meeting_talking_points_2026-05-29.md` |
| Optional: multi-seed intermediate fine-tuning | 2026-05-30 | 2026-06-07 | Repeat 10% and 20% settings across additional seeds if supervisor agrees | Proposed | `plans/plan_next_2_weeks.md` |

## Current main decision

The dissertation should be framed around reproducible baselines, strict transfer failure, and target-domain fine-tuning recovery. The 20% intermediate fine-tuning result should be described as the best current seed-42 recovery result unless additional seeds are run. The TELLER-like pilot is supporting analysis only.
