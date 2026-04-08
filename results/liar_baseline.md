# LIAR Baseline Results

> Purpose: record the current LIAR in-domain binary baseline results, including the sparse baseline, transformer baselines, seed-stability results, and the current main interpretation.

## 1) Run info

- Latest update: 2026-04-08
- Evaluation setting: **in-domain (LIAR → LIAR)**
- Main input text: **statement**
- Main notebooks:
  - `notebooks/01_liar_load.ipynb`
  - `notebooks/02_tfidf_baseline.ipynb`
  - `notebooks/03_bert_baseline.ipynb`
  - `notebooks/04_bert_weighted_baseline.ipynb`
  - `notebooks/05_roberta_baseline.ipynb`
- Main result files:
  - `results/baseline_results_summary.md`
  - `results/liar_baseline.md`
  - `results/bert_seed_sweep_results.md`
  - `results/bert_weighted_seed_sweep_results.md`
  - `results/liar_roberta_baseline_run_output.md`

---

## 2) Dataset

- Dataset: **LIAR**
- Files used:
  - `train.tsv`
  - `valid.tsv`
  - `test.tsv`
- Text field used for modelling: `statement`

### Split sizes

- Train: 10240
- Valid: 1284
- Test: 1267

### Binary mapping used in this project

- **REAL (0):** `true`, `mostly-true`, `half-true`
- **FAKE (1):** `barely-true`, `false`, `pants-fire`

### Label distribution after binary mapping

**Train**
- REAL: 5752
- FAKE: 4488

**Valid**
- REAL: 668
- FAKE: 616

**Test**
- REAL: 714
- FAKE: 553

---

## 3) Baseline development path

The LIAR binary baseline development progressed through the following stages:

1. **TF-IDF + Logistic Regression**
2. **BERT-base**
3. **BERT-base + weighted loss**
4. **RoBERTa-base**

This progression reflects a move from a sparse lexical baseline toward stronger transformer baselines, with later experiments focusing on improving class balance rather than only chasing small gains on linear models.

---

## 4) Main results overview

| Model | Accuracy | Macro-F1 | REAL Recall | FAKE Recall | Notes |
|---|---:|---:|---:|---:|---|
| TF-IDF + Logistic Regression | 0.6235 | 0.6005 | 0.7661 | 0.4394 | Final sparse baseline |
| BERT-base (3-seed mean) | 0.6369 ± 0.0028 | 0.6169 ± 0.0054 | — | — | Mean over seeds 42, 52, 62 |
| BERT-base + weighted loss (3-seed mean) | 0.6404 ± 0.0078 | 0.6304 ± 0.0081 | 0.7129 ± 0.0194 | 0.5467 ± 0.0241 | Current primary model |
| RoBERTa-base (single run) | 0.6504 | 0.6262 | 0.8025 | 0.4539 | Single run only |

---

## 5) Historical sparse baseline: TF-IDF + Logistic Regression

### Version 1 result
The initial TF-IDF baseline used minimal cleaning and did not yet use the validation split systematically for model selection.

- Accuracy: `0.6196`
- Macro-F1: `0.5935`

### Version 2 result
Version 2 introduced a more systematic validation-based workflow:

- preprocessing comparison on the validation split
- TF-IDF setting comparison on the validation split
- model selection based primarily on validation **Macro-F1**
- final retraining on **train + valid**
- single final evaluation on the **test split**

Final selected Version 2 configuration:

- Preprocess: `P0_minimal`
- `ngram_range=(1,2)`
- `min_df=2`
- `max_df=1.0`

Final Version 2 test result:

- Accuracy: `0.6235`
- Macro-F1: `0.6005`

### Difference vs Version 1

- Accuracy delta: `+0.0039`
- Macro-F1 delta: `+0.0070`

### TF-IDF confusion matrix

Label order: `[REAL, FAKE]`

```text
[[547 167]
 [310 243]]
````

### TF-IDF classification report

```text
              precision    recall  f1-score   support

        REAL     0.6383    0.7661    0.6964       714
        FAKE     0.5927    0.4394    0.5047       553

    accuracy                         0.6235      1267
   macro avg     0.6155    0.6028    0.6005      1267
weighted avg     0.6184    0.6235    0.6127      1267
```

### Main TF-IDF interpretation

The TF-IDF baseline showed that stronger preprocessing did **not** help in the current LIAR binary setup. Minimal preprocessing performed best, suggesting that aggressive normalisation may remove useful lexical cues in short political statements.

However, the remaining limitation of the sparse baseline was clear: the model still favoured the **REAL** class and achieved weak recall on **FAKE**.

---

## 6) Unweighted BERT baseline

The unweighted BERT baseline was fine-tuned on LIAR and evaluated across **3 random seeds**.

### Per-run results

* Seed `42`: best epoch `2`, valid accuracy `0.6386`, valid macro-F1 `0.6309`, test accuracy `0.6401`, test macro-F1 `0.6231`
* Seed `52`: best epoch `3`, valid accuracy `0.6472`, valid macro-F1 `0.6387`, test accuracy `0.6346`, test macro-F1 `0.6132`
* Seed `62`: best epoch `3`, valid accuracy `0.6394`, valid macro-F1 `0.6288`, test accuracy `0.6361`, test macro-F1 `0.6145`

### Mean and standard deviation

* Validation accuracy: `0.6417 ± 0.0047`
* Validation macro-F1: `0.6328 ± 0.0052`
* Test accuracy: `0.6369 ± 0.0028`
* Test macro-F1: `0.6169 ± 0.0054`

### Seed-42 test confusion matrix

```text
[[540 174]
 [282 271]]
```

### Seed-42 classification report

```text
              precision    recall  f1-score   support

        REAL     0.6569    0.7563    0.7031       714
        FAKE     0.6090    0.4901    0.5431       553

    accuracy                         0.6401      1267
   macro avg     0.6330    0.6232    0.6231      1267
weighted avg     0.6360    0.6401    0.6333      1267
```

### Main interpretation

Compared with the TF-IDF baseline, BERT consistently improved both accuracy and macro-F1. The gain was stable across seeds, which makes the result much more trustworthy than a single run.

However, the model still showed a clear tendency to favour the **REAL** class, and **FAKE recall** remained relatively low.

---

## 7) Weighted BERT baseline (current primary model)

To address the class-balance weakness of the unweighted BERT baseline, a separate weighted-loss experiment was created.

Class weights were computed from the **train split only** and applied **only in the training loss**.

Example weights from the successful weighted setup:

* REAL (0): `0.8901`
* FAKE (1): `1.1408`

### Per-run results

* Seed `42`: best epoch `2`, valid accuracy `0.6425`, valid macro-F1 `0.6407`, test accuracy `0.6456`, test macro-F1 `0.6380`, REAL recall `0.7017`, FAKE recall `0.5732`
* Seed `52`: best epoch `2`, valid accuracy `0.6456`, valid macro-F1 `0.6421`, test accuracy `0.6440`, test macro-F1 `0.6315`, REAL recall `0.7353`, FAKE recall `0.5262`
* Seed `62`: best epoch `3`, valid accuracy `0.6550`, valid macro-F1 `0.6519`, test accuracy `0.6314`, test macro-F1 `0.6218`, REAL recall `0.7017`, FAKE recall `0.5407`

### Mean and standard deviation

* Validation accuracy: `0.6477 ± 0.0065`
* Validation macro-F1: `0.6449 ± 0.0061`
* Test accuracy: `0.6404 ± 0.0078`
* Test macro-F1: `0.6304 ± 0.0081`
* REAL recall: `0.7129 ± 0.0194`
* FAKE recall: `0.5467 ± 0.0241`

### Seed-42 weighted test confusion matrix

```text
[[501 213]
 [236 317]]
```

### Seed-42 weighted classification report

```text
              precision    recall  f1-score   support

        REAL     0.6798    0.7017    0.6906       714
        FAKE     0.5981    0.5732    0.5854       553

    accuracy                         0.6456      1267
   macro avg     0.6389    0.6375    0.6380      1267
weighted avg     0.6441    0.6456    0.6447      1267
```

### Why weighted BERT is the current primary model

Weighted BERT is currently treated as the **main model** because:

* it gives the **best mean Macro-F1** among the tested models,
* it improves over the unweighted BERT baseline,
* it substantially improves **FAKE recall**,
* it produces a better balance between the two classes.

### Improvement relative to the unweighted BERT mean

* Accuracy delta: `+0.0034`
* Macro-F1 delta: `+0.0135`

The most important improvement is not the small gain in accuracy, but the more meaningful gain in **Macro-F1** and the stronger ability to identify the **FAKE** class.

---

## 8) RoBERTa baseline

A separate RoBERTa baseline was also created under the same overall LIAR binary setup.

### RoBERTa result

* Best epoch: `3`
* Validation accuracy: `0.6558`
* Validation macro-F1: `0.6435`
* Test accuracy: `0.6504`
* Test macro-F1: `0.6262`

### Confusion matrix

```text
[[573 141]
 [302 251]]
```

### Classification report

```text
              precision    recall  f1-score   support

        REAL     0.6549    0.8025    0.7212       714
        FAKE     0.6403    0.4539    0.5312       553

    accuracy                         0.6504      1267
   macro avg     0.6476    0.6282    0.6262      1267
weighted avg     0.6485    0.6504    0.6383      1267
```

### Interpretation

RoBERTa currently gives the **highest single-run accuracy**, but it does **not** outperform weighted BERT on Macro-F1. It also shows weaker **FAKE recall** than the weighted BERT setup.

For this reason, RoBERTa is currently treated as an important comparison model, but **not** the primary model.

---

## 9) Direct comparison of the current main baselines

### Weighted BERT vs TF-IDF

* Accuracy delta: `+0.0169`
* Macro-F1 delta: `+0.0299`

### Weighted BERT vs unweighted BERT

* Accuracy delta: `+0.0034`
* Macro-F1 delta: `+0.0135`

### Weighted BERT vs RoBERTa

* Accuracy delta: `-0.0100`
* Macro-F1 delta: `+0.0042`

These comparisons show the current trade-off clearly:

* **RoBERTa** is slightly stronger on raw test accuracy
* **weighted BERT** is stronger on Macro-F1 and class balance

Because this project treats balanced performance as more important than accuracy alone, weighted BERT is the more suitable main model.

---

## 10) Literature comparison (short)

The original LIAR paper introduced the dataset as a **6-class benchmark** of short political statements. That paper is useful as dataset background, but its results are **not directly comparable** to the current binary setup.

A more recent line of work reports stronger binary LIAR results with transformer-based models, which confirms that the current project is operating in the correct model family, but still below more advanced systems.

The current project position is therefore:

* clearly stronger than a simple sparse baseline,
* clearly improved by transformer fine-tuning,
* further improved by weighted loss,
* still not close to more advanced state-of-the-art systems reported in the literature.

---

## 11) Main interpretation

The current results suggest four main conclusions.

### 1. Transformer baselines consistently outperform the TF-IDF baseline

Both BERT and RoBERTa improve over the sparse baseline, showing that contextual transformer representations are useful for LIAR binary fake news detection.

### 2. The gain from TF-IDF to BERT is stable but moderate

The BERT 3-seed mean confirms that the improvement is real and stable, but not dramatic. This suggests that LIAR remains a challenging dataset even for stronger neural models.

### 3. Class imbalance in predictions is a central issue

Across models, there is a repeated tendency to perform better on **REAL** than on **FAKE**. This is one of the main reasons why Macro-F1 remains limited.

### 4. Weighted loss is an effective and interpretable improvement

Among the tested neural baselines, weighted BERT gives the best overall class-balanced result. It improves **FAKE recall** without sacrificing overall performance too heavily, which makes it the most appropriate primary model for the current study.

---

## 12) Current conclusion

At the current stage of the project:

* **TF-IDF + Logistic Regression** is the main traditional baseline.
* **BERT-base** is the main unweighted neural baseline.
* **BERT-base + weighted loss** is the current **primary model**.
* **RoBERTa-base** is an important comparison model with higher accuracy but weaker class balance.

The strongest current conclusion is that **weighted BERT** offers the best balance between the two classes and the best mean Macro-F1 among the tested baselines.

---

## 13) Next priorities

The next priorities are no longer simple linear-model comparisons.

The main next steps are:

1. **error analysis** of the weighted BERT model,
2. **literature review expansion**,
3. **cross-dataset / cross-domain pipeline design and implementation**.

Optional additional model work, if time allows:

* RoBERTa + weighted loss
* statement vs statement + context comparison

---

## 14) Notes

* This file should now be treated as the main detailed LIAR baseline record.
* The shorter high-level summary should stay in `results/baseline_results_summary.md`.
* Older TF-IDF-only “next steps” such as LinearSVC comparison should no longer be treated as the main direction of the project.

