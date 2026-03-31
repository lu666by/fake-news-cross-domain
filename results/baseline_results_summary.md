# LIAR Baseline Results Summary

## Task
This summary reports the current **LIAR in-domain binary baseline** using **TF-IDF + Logistic Regression**.  
The purpose of Version 2 was to improve the original baseline and make model selection more systematic by using the **validation split** for comparison before final testing.

## Dataset and setup
The experiments use the **LIAR** dataset in an **in-domain (LIAR → LIAR)** setting.  
The text field used for modelling is **statement** only.

Binary mapping used in this project:
- **REAL (0):** `true`, `mostly-true`, `half-true`
- **FAKE (1):** `barely-true`, `false`, `pants-fire`

Split sizes:
- Train: 10240
- Valid: 1284
- Test: 1267

## Version 1 reference
Version 1 was the initial TF-IDF + Logistic Regression baseline with only minimal text cleaning.

- **Accuracy:** 0.6196
- **Macro-F1:** 0.5935

## Version 2 approach
Version 2 introduced a more systematic validation-based workflow.  
Two types of comparisons were carried out on the **validation split**:

1. **Preprocessing comparison**
   - `P0_minimal`
   - `P1_lower`
   - `P2_lower_stopwords`
   - `P3_lower_stopwords_stemming`

2. **TF-IDF comparison**
   - `ngram_range=(1,2)`
   - `min_df` and `max_df` varied across multiple settings

The model selection rule prioritised **Macro-F1** on the validation split, with **Accuracy** used as a secondary criterion.

## Main validation findings
The preprocessing comparison showed that stronger preprocessing did **not** improve results in the current LIAR binary setup.

- `P0_minimal` and `P1_lower` gave the same validation result
- stronger preprocessing with stopword removal and stemming performed worse

Under the best preprocessing setting (`P0_minimal`), the best validation configuration was:

- **Exp ID:** E6
- **Preprocess:** `P0_minimal`
- **ngram_range:** `(1,2)`
- **min_df:** `2`
- **max_df:** `1.0`
- **Validation Accuracy:** `0.6231`
- **Validation Macro-F1:** `0.6123`

Although **E5** had slightly higher validation Accuracy, **E6** was selected because it had the best validation **Macro-F1**, which was treated as the primary model selection metric.

## Final Version 2 test result
The selected configuration was retrained on **train + valid** and evaluated once on the **test split**.

- **Accuracy:** 0.6235
- **Macro-F1:** 0.6005

Difference vs Version 1:
- **Accuracy delta:** +0.0039
- **Macro-F1 delta:** +0.0070

## Error pattern
The confusion matrix for the final Version 2 result is:

```text
[[547 167]
 [310 243]]
````

Label order: `[REAL, FAKE]`

This shows that the model still performs better on the **REAL** class than on the **FAKE** class.
A substantial number of **FAKE** examples are still misclassified as **REAL**, which helps explain why Macro-F1 remains limited.

## Interpretation

Version 2 is an improvement over Version 1, but the gain is still modest.
The validation results suggest that, for short LIAR political statements, stronger preprocessing may remove or distort useful lexical cues rather than helping the model.
The remaining limitation is therefore likely to be more related to **feature representation** and **classifier behaviour** than to simple text cleaning alone.

## Next step

The next baseline improvement stage will compare:

* Logistic Regression with `class_weight="balanced"`
* `LinearSVC`

This will help determine whether the remaining weakness is mainly due to class handling or classifier choice before moving to stronger models such as BERT.
