# Literature Review (Draft)

**Project:** Cross-dataset Generalisation for Fake News Detection  
**Date:** 2025-05-09  
**Status:** Draft — to be expanded with more citations and sub-sections

> **Note for expansion:** Each section needs more citations added before the final thesis. The target is 3–5 papers per section, with explicit contribution + limitation per paper. See `literature_review_requirements_note.md` for full improvement checklist.

---

## 2.1 Fake News Detection Datasets and LIAR

Research in fake news detection has depended heavily on the availability of labelled datasets. Several benchmark datasets have been established, each with different scope, label schemes, and domain coverage.

Wang (2017) introduced the LIAR dataset, one of the most widely used benchmarks in fake news detection research. LIAR was collected from PolitiFact.com and contains 12,836 labelled political statements. Each statement was assessed by expert fact-checkers and assigned one of six truthfulness labels: *true*, *mostly-true*, *half-true*, *barely-true*, *false*, and *pants-fire*. Metadata including speaker identity, political affiliation, and the context of the statement is also provided. The contribution of LIAR is significant: it offers a large-scale, naturally occurring political fake news corpus with fine-grained truthfulness labels. However, the six-class scheme presents a challenge for binary classification models, as the boundary between adjacent labels — particularly between *half-true* and *barely-true* — is ambiguous. This boundary ambiguity makes the task both harder and more realistic. Many subsequent studies map the six labels into a binary scheme (real / fake), following Wang's original suggestion.

Shu et al. (2020) released FakeNewsNet, a dataset that goes beyond claim text to include social context information such as article content, news propagation paths, and user engagement signals on social media. FakeNewsNet covers two domains: political news (sourced from PolitiFact) and entertainment news (sourced from GossipCop). The multi-domain structure of FakeNewsNet makes it particularly suitable for studying cross-domain generalisation. However, the social context features require external data access and are not always easy to use in all experimental settings, especially when only claim text is available.

Augenstein et al. (2019) presented MultiFC at EMNLP 2019, the largest publicly available dataset of naturally occurring fact-checked claims at the time. MultiFC aggregates claims from 26 English-language fact-checking websites, annotated by expert journalists, and includes associated evidence text. The dataset covers multiple domains — politics, science, and entertainment — and is notable for its diversity of sources and label schemes. MultiFC achieved a best Macro-F1 of only 49.2% in the original paper, reflecting how challenging cross-source veracity prediction is. The main limitation of MultiFC is the inconsistency in annotation standards across 26 different websites, which adds label noise and makes direct comparison between sources difficult.

These datasets vary considerably in domain, label scheme, and the kind of information they provide. This variation means that a model trained on LIAR may not perform well on FakeNewsNet or MultiFC, and vice versa. The mismatch between datasets — in terms of language style, topic focus, and annotation criteria — is a core motivation for studying cross-dataset generalisation.

---

## 2.2 Traditional and Transformer-Based Fake News Detection

The field of fake news detection has evolved from hand-crafted feature approaches to pre-trained language model fine-tuning. Each stage has contributed to our understanding of how linguistic signals relate to truthfulness.

Early studies showed that language style itself carries veracity signals. Rashkin et al. (2017) analysed the linguistic characteristics of fake news across different truthfulness levels, using the LIAR dataset. They found that deceptive statements tend to use more hedging language, stronger subjective sentiment, and fewer assertive phrases compared to truthful statements. This work demonstrated that even relatively simple linguistic features — captured by n-gram models — can be informative for veracity prediction. However, these models are highly domain-specific: features that distinguish true and false statements in political discourse may not transfer to entertainment or scientific domains.

Pérez-Rosas et al. (2018) further explored the use of linguistic features — including lexical, syntactic, and psycholinguistic features — for fake news detection. Their results confirmed that feature-based classifiers can achieve meaningful performance, but they also showed that performance drops significantly when models are tested on out-of-domain data. This finding highlighted the generalisation problem as a fundamental challenge for feature-based approaches.

A major shift occurred with the introduction of pre-trained language models. Devlin et al. (2019) proposed BERT (Bidirectional Encoder Representations from Transformers), which learns contextual text representations through pre-training on large corpora using two objectives: masked language modelling (MLM) and next sentence prediction (NSP). BERT demonstrated strong performance across a wide range of NLP tasks through fine-tuning on task-specific labelled data. The contribution of BERT is foundational: it showed that deep bidirectional context modelling can capture subtle semantic nuances that earlier models missed. BERT's limitation, as later identified, is that its pre-training procedure was sub-optimal due to undertrained configurations.

Liu et al. (2019) introduced RoBERTa (Robustly Optimized BERT Pretraining Approach), which revisited and improved BERT's pre-training by training on larger datasets, removing the NSP objective, and using dynamic masking. RoBERTa achieved state-of-the-art results on GLUE, RACE, and SQuAD benchmarks, outperforming BERT while using the same model architecture. RoBERTa has since become a strong baseline for text classification tasks, including fake news detection, due to its improved language understanding. The limitation of RoBERTa and similar models is that they are fine-tuned on a fixed training domain and may not generalise well when the test distribution differs significantly.

Papageorgiou et al. (2025) conducted a large-scale comparison of current methods across multiple fake news datasets, including LIAR and FakeNewsNet. The study compared traditional models, BERT-based classifiers, and LLM-based approaches, finding that performance varies substantially across datasets. This multi-dataset evaluation highlights that no single model achieves consistently strong results across all benchmarks. Importantly, this study evaluates each dataset separately — training and testing on the same dataset — rather than testing strict cross-dataset transfer. The distinction matters: multi-dataset evaluation does not directly measure a model's ability to transfer from one domain to another.

---

## 2.3 LLM and Reasoning-Based Fake News Detection

Recent advances in large language models have opened new directions for fake news detection. Rather than relying solely on fine-tuned classifiers, a growing body of research explores the use of LLMs for generating explanations, structured reasoning, and logic-guided predictions.

Liu et al. (2024) proposed TELLER (Trustworthy framEwork for expLainabLe, gEneRalizable and controllable fake news detection), published at Findings of ACL 2024. TELLER addresses three limitations of existing approaches: the lack of explainability in neural classifiers, poor generalisation across domains, and the risks of integrating LLMs without control mechanisms. The framework operates through two systems: a cognition system, which uses human-designed logical predicates to prompt an LLM and generate structured logic atoms from the input claim; and a decision system, which learns generalizable logic rules to aggregate these atoms and produce a prediction. On the LIAR binary task, TELLER reports an accuracy of 0.6773 and Macro-F1 of 0.6697, which is higher than standard BERT and RoBERTa fine-tuned baselines. The key limitation of TELLER is its dependency on the OpenAI API for the logic atom generation step, which introduces cost, rate limits, and dependency on an external service. The logic predicates also require human expertise to design, making the system less straightforward to reproduce or adapt.

Hu et al. (2024) examined the dual role of LLMs in the fake news ecosystem — as a potential tool for generating disinformation (the "bad actor" role) and as a tool for detecting it (the "good advisor" role). This line of research is important because it shows that LLMs are not simply solutions to fake news detection — they are also part of the problem. Understanding both roles is necessary for developing realistic assessments of LLM-based detection systems.

Pan et al. (2023) proposed a program-guided reasoning approach for fact-checking complex claims, presented at ACL 2023. By decomposing complex claims into a sequence of structured reasoning steps — expressed as programs — the system produces both a prediction and an interpretable reasoning chain. This method demonstrates that structured reasoning can improve both accuracy and explainability on complex, multi-step claims. The limitation is that this approach is more computationally expensive and harder to adapt than simple classifier fine-tuning.

Overall, LLM-based and reasoning-based approaches show strong performance and improved explainability, but they come with higher system complexity, API costs, and more demanding compute requirements. For resource-constrained research settings, these methods are important as reference points in the literature rather than directly reproducible baselines.

---

## 2.4 Class Imbalance and Evaluation Metrics

Class imbalance is a common challenge in fake news detection datasets. Models trained on imbalanced data tend to favour the majority class, leading to poor performance on the minority class.

Henning et al. (2023) conducted a comprehensive survey of class imbalance problems in NLP, reviewing methods including oversampling, undersampling, data augmentation, and loss function weighting. The survey found that class-weighted loss functions are often effective in practice for text classification tasks, as they directly adjust the contribution of each class during training without requiring data modification. The paper also discusses the choice of evaluation metric: accuracy is misleading under class imbalance, and Macro-F1 — which weights each class equally — is recommended as a more informative metric.

Johnson and Khoshgoftaar (2019) surveyed class imbalance approaches specifically in the context of deep learning, covering a wider range of techniques including ensemble methods and cost-sensitive learning. They found that the optimal strategy depends on the degree of imbalance and the task, but that weighted loss functions are consistently competitive across scenarios.

In the context of fake news detection on LIAR, the binary mapping from six labels can produce a slight class imbalance depending on the mapping chosen. Models trained without addressing this imbalance tend to have higher REAL recall but lower FAKE recall. Since the real-world cost of missing a fake news item (false negative) is typically higher than wrongly flagging a real item (false positive), FAKE recall is an important supplementary metric alongside Macro-F1.

---

## 2.5 Robustness and Cross-Dataset Generalisation

Cross-dataset generalisation is one of the most important unsolved problems in fake news detection. A model that performs well on one dataset often drops significantly when tested on another.

Wang et al. (2022) surveyed robustness research in NLP, covering domain shift, adversarial examples, and dataset bias. The survey found that models fine-tuned on a specific dataset often rely on dataset-specific patterns (shortcuts or spurious correlations) rather than general linguistic signals of truthfulness. This leads to brittle behaviour when the test distribution differs from training. In fake news detection, different datasets come from different sources, platforms, and annotation processes, which creates substantial distribution shifts between them.

Gururangan et al. (2020) proposed Domain-Adaptive Pretraining (DAPT), a method in which a pre-trained language model is further pre-trained on domain-specific unlabelled text before task-specific fine-tuning. DAPT showed consistent improvements across a range of domain-specific tasks, suggesting that bridging the gap between the general pre-training distribution and the target task domain can improve both in-domain and cross-domain performance. This approach is directly relevant to cross-dataset fake news detection: by adapting the language model to the language style of a target dataset before fine-tuning, it may be possible to reduce the performance drop caused by domain shift.

Silva et al. (2021) proposed a method that explicitly addresses cross-domain fake news detection by embracing domain differences rather than treating them as noise. Their work showed that recognising and modelling the differences between source and target domains — rather than ignoring them — improves cross-domain performance. This paper is one of the earlier works to frame fake news detection as a cross-domain problem, establishing the importance of this research direction.

Papageorgiou et al. (2025) provided evidence from multi-dataset evaluation that performance varies substantially across different fake news datasets, reinforcing the conclusion that no current method achieves robust cross-dataset generalisation. While their evaluation is multi-dataset rather than strictly cross-domain (models are trained on each dataset separately), the observed variability in results supports the argument that cross-dataset generalisation remains an open problem.

---

## 2.6 Research Gap

The literature reviewed above shows that fake news detection has made substantial progress in several areas. Large benchmark datasets are now available (Wang 2017; Shu et al. 2020; Augenstein et al. 2019). Transformer-based models have improved in-domain performance considerably compared to feature-based approaches (Devlin et al. 2019; Liu et al. 2019). More advanced systems have pushed performance further using LLM-based reasoning and explainability (Liu et al. 2024). The importance of class imbalance and evaluation metric choice is well understood (Henning et al. 2023).

However, several gaps remain.

First, most existing studies evaluate models only within a single dataset. Performance on in-domain LIAR, for example, does not tell us how well the model would perform on FakeNewsNet or MultiFC. Systematic cross-dataset generalisation — training on one dataset and testing on another — remains underexplored, particularly for transformer-based models.

Second, the impact of dataset-level differences — in label scheme, domain, and annotation style — on cross-dataset performance is not well understood. Even within the same family of models, different data sources lead to very different results, as shown by Papageorgiou et al. (2025).

Third, advanced systems like TELLER improve performance but require LLM API access and expert-designed components, making them difficult to reproduce or adapt in constrained research environments. There is a gap between high-performing, resource-intensive systems and accessible, reproducible baselines that can serve as reliable starting points for generalisation research.

Fourth, the relationship between class imbalance, evaluation metrics, and cross-domain transfer is not fully studied. When a model is transferred to a new dataset with a different class ratio, the effect on FAKE recall and Macro-F1 may differ from the in-domain case.

These gaps motivate the research direction of this dissertation: to establish reliable and reproducible in-domain baselines using weighted transformer models (BERT, RoBERTa), and to investigate how these baselines perform under cross-dataset transfer. The focus on training-efficient, locally reproducible models — without external API dependencies — addresses the accessibility gap identified above, while the systematic cross-dataset evaluation addresses the generalisation gap.
