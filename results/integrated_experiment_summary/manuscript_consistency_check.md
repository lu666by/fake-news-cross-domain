# Manuscript Consistency Check

- Date: 2026-05-25
- Scope: keyword coverage and contradiction scan after adding intermediate fine-tuning and TELLER-like pilot.

## `TELLER`

- Hits: `25`

- Paragraph 20: The LIAR experiments show that weighted RoBERTa obtains the highest mean Accuracy and Macro-F1 among the completed local baselines across five random seeds, although the gap to weighted BERT is modest. Weighted BERT obta
- Paragraph 21: The strict transfer experiments train on LIAR and evaluate on FakeNewsNet titles without target-domain adaptation. Under this setting, the weighted transformer baselines fall below a trivial majority-class (always-REAL)
- Paragraph 87: Summarise advanced LLM-based systems such as TELLER from the literature and explain why their reported results are not directly comparable with locally fine-tuned classifiers.
- Paragraph 101: Chapter 2 summarises datasets, traditional and transformer-based fake news detection, LLM-based reasoning systems, class imbalance, robustness, and cross-dataset generalisation. Chapter 3 describes the dataset preparatio
- Paragraph 122: Liu et al. [9] proposed TELLER, an LLM-based framework published at Findings of ACL 2024. TELLER addresses three limitations of existing approaches: the lack of explainability in neural classifiers, poor generalisation a
- Paragraph 126: Overall, LLM-based and reasoning-based approaches improve explainability and, in some setups, accuracy. They are important comparators, but they answer a different implementation question from this dissertation's control
- Paragraph 151: Third, advanced systems such as TELLER [9] and ARG [10] improve performance but are not directly comparable with standard local classifiers because they use different system designs, intermediate representations, and rea
- Paragraph 220: TELLER is reported only with the published aggregate LIAR Accuracy and Macro-F1 because the paper comparison is not the same locally saved classification-report setting as the project baselines.
- Paragraph 229: 4.6 Comparison with TELLER
- Paragraph 230: TELLER reports stronger LIAR binary performance, with Accuracy 0.6773 and Macro-F1 0.6697. However, TELLER is a different kind of system from the baselines evaluated in this dissertation. Rather than fine-tuning a text c
- Paragraph 260: This chapter first reports the strict cross-dataset evaluation, where models are trained on LIAR and tested directly on FakeNewsNet minimal titles. It then extends the analysis with intermediate target-domain fine-tuning
- Paragraph 300: Table 6.4. Integrated comparison of in-domain, direct transfer, intermediate fine-tuning, and TELLER-like pilot results.
- ... 13 more hits omitted for brevity.

## `TELLER-like`

- Hits: `9`

- Paragraph 21: The strict transfer experiments train on LIAR and evaluate on FakeNewsNet titles without target-domain adaptation. Under this setting, the weighted transformer baselines fall below a trivial majority-class (always-REAL)
- Paragraph 101: Chapter 2 summarises datasets, traditional and transformer-based fake news detection, LLM-based reasoning systems, class imbalance, robustness, and cross-dataset generalisation. Chapter 3 describes the dataset preparatio
- Paragraph 260: This chapter first reports the strict cross-dataset evaluation, where models are trained on LIAR and tested directly on FakeNewsNet minimal titles. It then extends the analysis with intermediate target-domain fine-tuning
- Paragraph 300: Table 6.4. Integrated comparison of in-domain, direct transfer, intermediate fine-tuning, and TELLER-like pilot results.
- Paragraph 303: 6.9 TELLER-like LLM Reasoning-Atoms Pilot
- Paragraph 304: A second exploratory experiment was added to test a simplified TELLER-like idea. Instead of asking an LLM to decide whether each item was REAL or FAKE, DeepSeek V4 Flash generated structured reasoning atoms such as emoti
- Paragraph 309: This transfer setting has five main limitations. First, LIAR statements and FakeNewsNet titles are different text fields, so the experiment combines dataset shift with input-format shift. Second, LIAR is mainly political
- Paragraph 318: As a supplementary observation rather than a main experimental finding, TELLER remains best treated as an advanced literature comparison. The local TELLER-like reasoning-atoms pilot is useful because it separates LLM-gen
- Paragraph 349: The first outcome is a reproducible LIAR binary baseline setup with fixed splits, consistent label mapping, and five-seed transformer evaluation. The second outcome is a class-sensitive comparison demonstrating that the

## `intermediate fine-tuning`

- Hits: `21`

- Paragraph 21: The strict transfer experiments train on LIAR and evaluate on FakeNewsNet titles without target-domain adaptation. Under this setting, the weighted transformer baselines fall below a trivial majority-class (always-REAL)
- Paragraph 209: The reported files in the results directory contain the saved summary tables, cross-dataset outputs, intermediate fine-tuning outputs, LLM reasoning-atoms pilot outputs, and error analysis. This means the dissertation nu
- Paragraph 297: 6.8 Intermediate Fine-Tuning with Target-Domain FakeNewsNet Titles
- Paragraph 298: The strict transfer results show that LIAR-trained transformer models do not move reliably to FakeNewsNet titles without adaptation. To test whether a small amount of target-domain supervision can correct this failure mo
- Paragraph 299: The target-domain fractions were 5%, 10%, and 20% of the FakeNewsNet training split. The 5% setting used 742 target examples, the 10% setting used 1,484 examples, and the 20% setting used 2,969 examples. The same held-ou
- Paragraph 300: Table 6.4. Integrated comparison of in-domain, direct transfer, intermediate fine-tuning, and TELLER-like pilot results.
- Paragraph 301: The intermediate fine-tuning results change the interpretation of the cross-dataset experiment. With no target-domain adaptation, the LIAR-trained weighted RoBERTa model is almost entirely FAKE-biased on the held-out Fak
- Paragraph 302: These results show that the poor direct transfer scores are not simply caused by the target dataset being impossible. Rather, the model needs enough labelled target-domain examples to recalibrate its decision boundary. I
- Paragraph 307: RQ5 asks how well LIAR-trained baselines transfer to FakeNewsNet minimal titles. Under strict direct transfer, the answer remains weak: the transformer models over-predict FAKE and perform below the always-REAL majority-
- Paragraph 309: This transfer setting has five main limitations. First, LIAR statements and FakeNewsNet titles are different text fields, so the experiment combines dataset shift with input-format shift. Second, LIAR is mainly political
- Paragraph 318: As a supplementary observation rather than a main experimental finding, TELLER remains best treated as an advanced literature comparison. The local TELLER-like reasoning-atoms pilot is useful because it separates LLM-gen
- Paragraph 321: The cross-dataset results have a stronger implication. A model can look strong on LIAR but fail badly when tested on another dataset. Intermediate fine-tuning shows that this failure is not permanent: with 10-20% labelle
- ... 9 more hits omitted for brevity.

## `target-domain adaptation`

- Hits: `4`

- Paragraph 21: The strict transfer experiments train on LIAR and evaluate on FakeNewsNet titles without target-domain adaptation. Under this setting, the weighted transformer baselines fall below a trivial majority-class (always-REAL)
- Paragraph 301: The intermediate fine-tuning results change the interpretation of the cross-dataset experiment. With no target-domain adaptation, the LIAR-trained weighted RoBERTa model is almost entirely FAKE-biased on the held-out Fak
- Paragraph 331: The highest-priority remaining next step is to repeat the intermediate fine-tuning experiment across multiple seeds, especially for the 10% and 20% target-domain settings. This would test whether the observed recovery fr
- Paragraph 354: The highest-priority remaining next step is to repeat the intermediate fine-tuning experiment across multiple seeds, especially for the 10% and 20% target-domain settings. This would test whether the observed recovery fr

## `cross-dataset`

- Hits: `38`

- Paragraph 0: Cross-Dataset Generalisation for Fake News Detection Using Reproducible Transformer-Based Baselines
- Paragraph 13: I, Boyu Lu, hereby declare that this thesis, titled "Cross-Dataset Generalisation for Fake News Detection Using Reproducible Transformer-Based Baselines", and the work presented in it are my own except where explicitly s
- Paragraph 19: This dissertation investigates reproducible fake news detection baselines with a focus on a binary fake news detection task and cross-dataset behaviour. The project compares a traditional TF-IDF and Logistic Regression b
- Paragraph 21: The strict transfer experiments train on LIAR and evaluate on FakeNewsNet titles without target-domain adaptation. Under this setting, the weighted transformer baselines fall below a trivial majority-class (always-REAL)
- Paragraph 22: Keywords: Fake news detection; Class imbalance; Cross-dataset generalisation; Transformer fine-tuning; Baseline evaluation; Distribution shift
- Paragraph 36: 6 Cross-Dataset Evaluation 	29
- Paragraph 43: 3.1 Overall experimental pipeline for cross-dataset fake news detection 	15
- Paragraph 99: An identification of research gaps in current literature concerning reproducible cross-dataset fake news detection.
- Paragraph 101: Chapter 2 summarises datasets, traditional and transformer-based fake news detection, LLM-based reasoning systems, class imbalance, robustness, and cross-dataset generalisation. Chapter 3 describes the dataset preparatio
- Paragraph 110: These datasets vary considerably in domain, label scheme, and the kind of information they provide. This variation means that a model trained on LIAR may not perform well on FakeNewsNet or MultiFC, and vice versa. The mi
- Paragraph 118: Papageorgiou et al. [8] conducted a large-scale comparison of current methods across multiple fake news datasets, including LIAR and FakeNewsNet. The study compared traditional models, BERT-based classifiers, and LLM-bas
- Paragraph 132: 2.5 Robustness and Cross-Dataset Generalisation
- ... 26 more hits omitted for brevity.

## `FakeNewsNet`

- Hits: `69`

- Paragraph 21: The strict transfer experiments train on LIAR and evaluate on FakeNewsNet titles without target-domain adaptation. Under this setting, the weighted transformer baselines fall below a trivial majority-class (always-REAL)
- Paragraph 44: 3.2 Binary label mapping and class distribution across LIAR and FakeNewsNet 	17
- Paragraph 49: 6.1 Macro-F1 on LIAR and FakeNewsNet combined titles 	31
- Paragraph 50: 6.2 Class-level recall on FakeNewsNet combined titles 	32
- Paragraph 51: 6.3 Majority baseline comparison on FakeNewsNet combined titles 	32
- Paragraph 57: 3.1 Dataset splits and label distributions for LIAR and FakeNewsNet 	15
- Paragraph 65: 6.2 LIAR-to-FakeNewsNet title transfer results 	30
- Paragraph 66: 6.3 Majority-class (always-REAL) reference baseline on FakeNewsNet minimal titles 	30
- Paragraph 79: Many fake news detection studies focus on in-domain evaluation, where the model is trained and tested on splits from the same dataset. This setting is useful, but it can overestimate real-world reliability. A detector tr
- Paragraph 82: The aim of this dissertation is to evaluate how selected LIAR-trained text classifiers perform in-domain and when transferred to FakeNewsNet titles, with attention to FAKE recall and the role of class weighting.
- Paragraph 88: Compare LIAR-trained classifiers on FakeNewsNet titles under strict transfer, and report the gap against a trivial always-REAL class-prior baseline.
- Paragraph 98: A strict LIAR-to-FakeNewsNet title transfer evaluation that demonstrates a severe generalisation drop and benchmarks it against a trivial always-REAL baseline.
- ... 57 more hits omitted for brevity.

## `Macro-F1`

- Hits: `50`

- Paragraph 19: This dissertation investigates reproducible fake news detection baselines with a focus on a binary fake news detection task and cross-dataset behaviour. The project compares a traditional TF-IDF and Logistic Regression b
- Paragraph 20: The LIAR experiments show that weighted RoBERTa obtains the highest mean Accuracy and Macro-F1 among the completed local baselines across five random seeds, although the gap to weighted BERT is modest. Weighted BERT obta
- Paragraph 21: The strict transfer experiments train on LIAR and evaluate on FakeNewsNet titles without target-domain adaptation. Under this setting, the weighted transformer baselines fall below a trivial majority-class (always-REAL)
- Paragraph 49: 6.1 Macro-F1 on LIAR and FakeNewsNet combined titles 	31
- Paragraph 80: Another issue is class imbalance and class-level behaviour. A model may achieve acceptable Accuracy while still missing many FAKE examples. In practical fake news detection, this is a serious limitation because false neg
- Paragraph 85: Evaluate the impact of class-weighted loss functions on Macro-F1 and FAKE recall under class imbalance.
- Paragraph 96: A class-sensitive analysis showing that class-weighted loss functions improve minority-class (FAKE) recall but result in modest Macro-F1 variations.
- Paragraph 109: Augenstein et al. [3] presented MultiFC at EMNLP 2019, the largest publicly available dataset of naturally occurring fact-checked claims at the time. MultiFC aggregates claims from 26 English-language fact-checking websi
- Paragraph 122: Liu et al. [9] proposed TELLER, an LLM-based framework published at Findings of ACL 2024. TELLER addresses three limitations of existing approaches: the lack of explainability in neural classifiers, poor generalisation a
- Paragraph 129: Henning et al. [13] conducted a comprehensive survey of class imbalance problems in NLP, reviewing methods including oversampling, undersampling, data augmentation, and loss function weighting. The survey found that clas
- Paragraph 131: In the context of fake news detection on LIAR, the binary mapping from six labels can produce a slight class imbalance depending on the mapping chosen. Models trained without addressing this imbalance tend to have higher
- Paragraph 152: Fourth, the relationship between class imbalance, evaluation metrics, and cross-domain transfer is not fully studied. When a model is transferred to a new dataset with a different class ratio, the effect on FAKE recall a
- ... 38 more hits omitted for brevity.

## Contradiction Scan

- `only evaluates direct cross-dataset transfer`: 0 hits
- `only evaluate direct cross-dataset transfer`: 0 hits
- `This thesis only`: 0 hits
- `strict transfer only`: 0 hits
- `without any target-domain adaptation`: 0 hits

Conclusion: no hard contradiction remains. Remaining uses of `without target-domain adaptation` refer specifically to the strict direct-transfer baseline and are paired with the added intermediate fine-tuning/adaptation discussion.
