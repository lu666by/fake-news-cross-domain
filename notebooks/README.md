# Notebooks

This folder contains the main experiment notebooks used in this MSc dissertation project.

The notebooks here are the **user’s own working versions** and form the main record of:

- dataset loading and inspection,
- sparse baseline experiments,
- transformer baseline experiments,
- weighted model extensions,
- and targeted follow-up comparison checks.

## Contents

- `01_liar_load.ipynb`  
  Load and inspect the LIAR dataset, including split sizes, binary label distribution, example statements, example contexts, and simple text statistics.

- `02_tfidf_baseline.ipynb`  
  Run the LIAR **TF-IDF + Logistic Regression** baseline, compare validation settings, and record the final sparse baseline result.

- `03_bert_baseline.ipynb`  
  Run the LIAR **BERT-base** baseline for binary classification.

- `04_bert_weighted_baseline.ipynb`  
  Run the LIAR **BERT-base + weighted loss** baseline.

- `05_roberta_baseline.ipynb`  
  Run the LIAR **RoBERTa-base** baseline as a stronger transformer comparison model.

- `06_roberta_weighted_baseline.ipynb`  
  Run the LIAR **RoBERTa-base + weighted loss** baseline, which is currently the strongest overall model line.

- `07_roberta_weighted_context_comparison.py`  
  Run a controlled comparison between:
  - `statement_only`
  - `statement + " [CTX] " + context`
  under the same weighted RoBERTa setup.

- `08_roberta_weighted_threshold_tuning.py`  
  Run validation-based threshold tuning for the weighted RoBERTa model and compare alternative decision thresholds.

## Recommended reading order

For reading or supervisor review, the recommended order is:

`01 -> 02 -> 03 -> 04 -> 05 -> 06 -> 07 -> 08`

This order reflects the actual development path of the project:

1. data loading and inspection,
2. traditional sparse baseline,
3. unweighted transformer baseline,
4. weighted BERT improvement,
5. unweighted RoBERTa comparison,
6. weighted RoBERTa extension,
7. context-based follow-up check,
8. threshold-tuning follow-up check.

## Current status

At the current stage of the project:

- the **TF-IDF** notebook provides the main traditional baseline,
- the **BERT** notebook provides the main unweighted neural baseline,
- the **weighted BERT** notebook remains important as the stronger **FAKE-recall** comparison model,
- the **weighted RoBERTa** notebook provides the current **strongest overall model**,
- the later follow-up scripts test the most direct next-step ideas suggested by error analysis.

## Important note

External GitHub repositories were used only as **implementation references**.

They do **not** replace the notebooks and scripts in this folder, which remain the primary record of the user’s own implementation and experiments.

External reference links should be listed in the project-level `README.md`.
