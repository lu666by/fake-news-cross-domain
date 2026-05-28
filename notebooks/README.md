# Notebooks

This folder keeps the original project workflow format: numbered notebooks/scripts in the order they were used.

## Main sequence

| # | File | Purpose |
|---|---|---|
| 01 | `01_liar_load.ipynb` | Load and inspect LIAR splits and binary label mapping |
| 02 | `02_tfidf_baseline.ipynb` | Deterministic TF-IDF + Logistic Regression baseline |
| 03 | `03_bert_baseline.ipynb` | Unweighted BERT baseline |
| 04 | `04_bert_weighted_baseline.ipynb` | Weighted BERT baseline |
| 05 | `05_roberta_baseline.ipynb` | Unweighted RoBERTa baseline |
| 06 | `06_roberta_weighted_baseline.ipynb` | Weighted RoBERTa baseline |
| 07 | `07_roberta_weighted_context_comparison.py` | Statement-only vs statement+context check |
| 08 | `08_roberta_weighted_threshold_tuning.py` | Validation-threshold scan |
| 09 | `09_cross_dataset_tfidf_liar_to_fakenewsnet.py` | TF-IDF LIAR-to-FakeNewsNet transfer |
| 10 | `10_cross_dataset_transformer_liar_to_fakenewsnet.py` | Transformer LIAR-to-FakeNewsNet transfer |
| 11 | `11_cross_dataset_results_summary_figures.py` | Cross-dataset summary tables and figures |
| 12 | `12_llm_reasoning_atoms_teller_like.py` | Exploratory TELLER-like reasoning-atoms pilot |
| 13 | `13_intermediate_finetuning_fakenewsnet.py` | Intermediate target-domain fine-tuning |

## Utility modules

- `liar_utils.py`
- `cross_dataset_utils.py`

## Current interpretation

The most important scripts for the current thesis argument are:

- `10_cross_dataset_transformer_liar_to_fakenewsnet.py`
- `13_intermediate_finetuning_fakenewsnet.py`
- `11_cross_dataset_results_summary_figures.py`

These support the main conclusion that strict direct transfer from LIAR to FakeNewsNet is unreliable, while intermediate target-domain fine-tuning can recover performance.
