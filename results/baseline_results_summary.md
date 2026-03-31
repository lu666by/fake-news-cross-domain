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

## 8.1 Why analysis

### Why analysis

#### 1) Why did TF-IDF tuning help?

The TF-IDF comparison suggests that moderate feature filtering helped the LIAR binary baseline, although the effect was relatively small. In the validation experiments, the best selected setting was **E6** (`ngram_range=(1,2)`, `min_df=2`, `max_df=1.0`), which achieved the strongest validation **Macro-F1**. By contrast, **E5** (`min_df=1`) achieved slightly higher validation Accuracy, but a lower Macro-F1, so it was not selected under the current model selection rule.

A likely explanation is that increasing `min_df` from `1` to `2` removed some very rare terms and rare bigrams that appeared in only one training document. In a short-text dataset such as LIAR, these extremely rare features are more likely to reflect accidental wording or dataset-specific noise than stable class-discriminative patterns. Removing them can make the feature space less sparse and help Logistic Regression learn more reliable weights, especially across both classes rather than mainly improving majority-style predictions.

At the same time, increasing `min_df` too much did not help. When `min_df` was increased further to `5` (**E8**), performance dropped slightly. This suggests that some low-frequency terms still carry useful information for distinguishing REAL from FAKE claims, and removing too many of them weakens the representation.

The comparison between **E6** and **E7** is also informative. These two settings produced identical validation results, even though `max_df` changed from `1.0` to `0.95`. This suggests that removing very high-frequency terms was not the main factor behind improvement in this run. In other words, the main gain seems to come more from filtering out very rare noisy features than from filtering out very common ones.

Overall, the TF-IDF results suggest that the best setting is a compromise: keep enough lexical detail to preserve useful cues, but remove the rarest features that are likely to add noise rather than signal.

#### 2) Why did minimal preprocessing perform better?

The preprocessing comparison gave a slightly counter-intuitive result. In many traditional text classification tasks, stronger preprocessing is expected to help. However, in the current LIAR binary setup, **minimal preprocessing (`P0_minimal`) and simple lowercasing (`P1_lower`) gave the same validation result**, while stronger preprocessing with stopword removal and stemming performed worse.

A likely explanation is that LIAR consists of **short political statements**, where each word contributes proportionally more information than it would in longer documents. Because the statements are short, aggressive preprocessing may remove or distort useful lexical cues too early. For example, stopword removal can delete function words that contribute to tone, emphasis, negation, or rhetorical structure. Even when such words are not individually strong features, in short claims they may still help preserve the original phrasing pattern.

Stemming may also reduce discriminative information. By collapsing different surface forms into the same stem, it can blur subtle differences in meaning, register, or factual framing. In a dataset such as LIAR, where the task is to classify brief and sometimes ambiguous claims, these small wording differences may still matter. Once those details are removed, the model may lose cues that help separate REAL and FAKE statements.

The current results are consistent with that interpretation. Lowercasing alone did not damage performance, which suggests that case information is not especially important here. However, once stopword removal and stemming were added, validation performance decreased. This indicates that the problem is not preprocessing in general, but rather that **stronger preprocessing removes useful information from already short texts**.

Overall, the results suggest that for LIAR, preserving the original wording is more helpful than aggressively normalising it. This is one reason why a relatively simple preprocessing setup performed best in the current baseline.
