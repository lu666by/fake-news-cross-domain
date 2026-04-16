# Notebooks

This folder contains the main notebooks and scripts used in this project.

## Files

- `01_liar_load.ipynb`  
  Load and inspect the LIAR dataset.

- `02_tfidf_baseline.ipynb`  
  Run the LIAR TF-IDF + Logistic Regression baseline.

- `03_bert_baseline.ipynb`  
  Run the LIAR unweighted BERT baseline.

- `04_bert_weighted_baseline.ipynb`  
  Run the LIAR weighted BERT baseline.

- `05_roberta_baseline.ipynb`  
  Run the LIAR unweighted RoBERTa baseline.

- `06_roberta_weighted_baseline.ipynb`  
  Run the LIAR weighted RoBERTa baseline.

- `07_roberta_weighted_context_comparison.py`  
  Compare `statement_only` vs `statement + [CTX] + context` under the weighted RoBERTa setup.

- `08_roberta_weighted_threshold_tuning.py`  
  Test validation-based threshold tuning for weighted RoBERTa.

## Recommended reading order

`01 -> 02 -> 03 -> 04 -> 05 -> 06 -> 07 -> 08`

## Current main model file

The current strongest overall model is the weighted RoBERTa setup, mainly recorded in:

- `06_roberta_weighted_baseline.ipynb`

## Note

The notebooks and scripts in this folder are the user’s own working files for this dissertation project.

External repositories were used only as implementation references and do not replace the files in this folder.
