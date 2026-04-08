# Notebooks

This folder contains the main experiment notebooks used in this MSc dissertation project.

The notebooks here are the **user’s own working versions** and form the main record of:

- dataset loading and inspection,
- sparse baseline experiments,
- transformer baseline experiments,
- and later model comparison updates.

## Contents

- `01_liar_load.ipynb`  
  Load and inspect the LIAR dataset, including split sizes, binary label distribution, example statements, example contexts, and simple text statistics.

- `02_tfidf_baseline.ipynb`  
  Run the LIAR **TF-IDF + Logistic Regression** baseline, compare validation settings, and record the final sparse baseline result.

- `03_bert_baseline.ipynb`  
  Run the LIAR **BERT-base** baseline for binary classification.

- `04_bert_weighted_baseline.ipynb`  
  Run the LIAR **BERT-base + weighted loss** baseline, which is currently the main class-balanced model.

- `05_roberta_baseline.ipynb`  
  Run the LIAR **RoBERTa-base** baseline as a stronger transformer comparison model.

## Recommended reading order

For reading or supervisor review, the recommended notebook order is:

`01 -> 02 -> 03 -> 04 -> 05`

This order reflects the actual development path of the project:

1. data loading and inspection,
2. traditional sparse baseline,
3. unweighted transformer baseline,
4. weighted transformer improvement,
5. stronger transformer comparison.

## Current status

At the current stage of the project:

- the **TF-IDF** notebook provides the main traditional baseline,
- the **BERT** notebook provides the main unweighted neural baseline,
- the **weighted BERT** notebook provides the current **primary model**,
- the **RoBERTa** notebook provides an important comparison model.

## Important note

External GitHub repositories were used only as **implementation references**.

They do **not** replace the notebooks in this folder, which remain the primary record of the user’s own implementation and experiments.

External reference links should be listed in the project-level `README.md`.
