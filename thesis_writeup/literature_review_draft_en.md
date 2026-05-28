# Literature Review (Draft)

**Project:** Cross-dataset Generalisation for Fake News Detection
**Date:** 2026-05-10
**Status:** Draft — second-round expansion (19 references; targeting 22 in next pass)

> **Note for expansion:** Each section now has 2–4 papers cited with explicit contribution + limitation. The next pass will add domain-adaptive language modelling for fake news, and strengthen the research gap section with one further cross-dataset reference. See `literature_review_requirements_note.md` for full improvement checklist.

---

## 2.1 Fake News Detection Datasets and LIAR

Research in fake news detection has depended heavily on the availability of labelled datasets. Several benchmark datasets have been established, each with different scope, label schemes, and domain coverage.

Wang [1] introduced the LIAR dataset, one of the most widely used benchmarks in fake news detection research. LIAR was collected from PolitiFact.com and contains 12,836 labelled political statements. Each statement was assessed by expert fact-checkers and assigned one of six truthfulness labels: *true*, *mostly-true*, *half-true*, *barely-true*, *false*, and *pants-fire*. Metadata including speaker identity, political affiliation, and the context of the statement is also provided. The contribution of LIAR is significant: it offers a large-scale, naturally occurring political fake news corpus with fine-grained truthfulness labels. However, the six-class scheme presents a challenge for binary classification models, as the boundary between adjacent labels — particularly between *half-true* and *barely-true* — is ambiguous. This boundary ambiguity makes the task both harder and more realistic. Many subsequent studies map the six labels into a binary scheme (real / fake), following Wang's original suggestion.

Shu et al. [2] released FakeNewsNet, a dataset that goes beyond claim text to include social context information such as article content, news propagation paths, and user engagement signals on social media. FakeNewsNet covers two domains: political news (sourced from PolitiFact) and entertainment news (sourced from GossipCop). The multi-domain structure of FakeNewsNet makes it particularly suitable for studying cross-domain generalisation. However, the social context features require external data access and are not always easy to use in all experimental settings, especially when only claim text is available.

Augenstein et al. [3] presented MultiFC at EMNLP 2019, the largest publicly available dataset of naturally occurring fact-checked claims at the time. MultiFC aggregates claims from 26 English-language fact-checking websites, annotated by expert journalists, and includes associated evidence text. The dataset covers multiple domains — politics, science, and entertainment — and is notable for its diversity of sources and label schemes. MultiFC achieved a best Macro-F1 of only 49.2% in the original paper, reflecting how challenging cross-source veracity prediction is. The main limitation of MultiFC is the inconsistency in annotation standards across 26 different websites, which adds label noise and makes direct comparison between sources difficult.

These datasets vary considerably in domain, label scheme, and the kind of information they provide. This variation means that a model trained on LIAR may not perform well on FakeNewsNet or MultiFC, and vice versa. The mismatch between datasets — in terms of language style, topic focus, and annotation criteria — is a core motivation for studying cross-dataset generalisation.

---

## 2.2 Traditional and Transformer-Based Fake News Detection

The field of fake news detection has evolved from hand-crafted feature approaches to pre-trained language model fine-tuning. Each stage has contributed to our understanding of how linguistic signals relate to truthfulness.

Early studies showed that language style itself carries veracity signals. Rashkin et al. [4] analysed the linguistic characteristics of fake news across different truthfulness levels, using the LIAR dataset. They found that deceptive statements tend to use more hedging language, stronger subjective sentiment, and fewer assertive phrases compared to truthful statements. This work demonstrated that even relatively simple linguistic features — captured by n-gram models — can be informative for veracity prediction. However, these models are highly domain-specific: features that distinguish true and false statements in political discourse may not transfer to entertainment or scientific domains.

Pérez-Rosas et al. [5] further explored the use of linguistic features — including lexical, syntactic, and psycholinguistic features — for fake news detection. Their results confirmed that feature-based classifiers can achieve meaningful performance, but they also showed that performance drops significantly when models are tested on out-of-domain data. This finding highlighted the generalisation problem as a fundamental challenge for feature-based approaches.

A major shift occurred with the introduction of pre-trained language models. Devlin et al. [6] proposed BERT (Bidirectional Encoder Representations from Transformers), which learns contextual text representations through pre-training on large corpora using two objectives: masked language modelling (MLM) and next sentence prediction (NSP). BERT demonstrated strong performance across a wide range of NLP tasks through fine-tuning on task-specific labelled data. The contribution of BERT is foundational: it showed that deep bidirectional context modelling can capture subtle semantic nuances that earlier models missed. BERT's limitation, as later identified, is that its pre-training procedure was sub-optimal due to undertrained configurations.

Liu et al. [7] introduced RoBERTa (Robustly Optimized BERT Pretraining Approach), which revisited and improved BERT's pre-training by training on larger datasets, removing the NSP objective, and using dynamic masking. RoBERTa achieved state-of-the-art results on GLUE, RACE, and SQuAD benchmarks, outperforming BERT while using the same model architecture. RoBERTa has since become a strong baseline for text classification tasks, including fake news detection, due to its improved language understanding. The limitation of RoBERTa and similar models is that they are fine-tuned on a fixed training domain and may not generalise well when the test distribution differs significantly.

Papageorgiou et al. [8] conducted a large-scale comparison of current methods across multiple fake news datasets, including LIAR and FakeNewsNet. The study compared traditional models, BERT-based classifiers, and LLM-based approaches, finding that performance varies substantially across datasets. This multi-dataset evaluation highlights that no single model achieves consistently strong results across all benchmarks. Importantly, this study evaluates each dataset separately — training and testing on the same dataset — rather than testing strict cross-dataset transfer. The distinction matters: multi-dataset evaluation does not directly measure a model's ability to transfer from one domain to another.

---

## 2.3 LLM and Reasoning-Based Fake News Detection

Recent advances in large language models have opened new directions for fake news detection. Rather than relying solely on fine-tuned classifiers, a growing body of research explores the use of LLMs for generating explanations, structured reasoning, and logic-guided predictions.

Liu et al. [9] proposed TELLER (Trustworthy framEwork for expLainabLe, gEneRalizable and controllable fake news detection), published at Findings of ACL 2024. TELLER addresses three limitations of existing approaches: the lack of explainability in neural classifiers, poor generalisation across domains, and the risks of integrating LLMs without control mechanisms. The framework operates through two systems: a cognition system, which uses human-designed logical predicates to prompt an LLM and generate structured logic atoms from the input claim; and a decision system, which learns generalizable logic rules to aggregate these atoms and produce a prediction. On the LIAR binary task, TELLER reports an accuracy of 0.6773 and Macro-F1 of 0.6697, which is higher than standard BERT and RoBERTa fine-tuned baselines. The key limitation of TELLER is its dependency on the OpenAI API for the logic atom generation step, which introduces cost, rate limits, and dependency on an external service. The logic predicates also require human expertise to design, making the system less straightforward to reproduce or adapt.

Hu et al. [10] examined the dual role of LLMs in the fake news ecosystem — as a potential tool for generating disinformation (the "bad actor" role) and as a tool for detecting it (the "good advisor" role). Their empirical study shows that GPT-3.5 prompted directly to predict fake or real news consistently underperforms a fine-tuned BERT on both Chinese and English benchmarks (Weibo21 and GossipCop), but that LLM-generated rationales, when used as side input to a small fine-tuned model rather than as the predictor, produce a stronger system than either model alone. Their proposed Adaptive Rationale Guidance (ARG) network frames the LLM as an *advisor* rather than a *detector*. The main limitation is that ARG still requires LLM API access during training, which retains some of the cost barriers identified for TELLER.

Pelrine et al. [11] provided one of the first systematic comparisons of LLM prompting strategies for fake news detection across multiple datasets. Their results showed that LLM-only baselines, even with carefully designed prompts, do not consistently match fine-tuned smaller models on standard benchmarks. This finding is consistent with Hu et al. [10] and supports the more cautious view that LLMs alone are not yet a drop-in replacement for fine-tuned classifiers in this task. The limitation of this work is that it does not propose a new system, but its diagnostic value is clear.

Pan et al. [12] proposed a program-guided reasoning approach for fact-checking complex claims, presented at ACL 2023. By decomposing complex claims into a sequence of structured reasoning steps — expressed as programs — the system produces both a prediction and an interpretable reasoning chain. This method demonstrates that structured reasoning can improve both accuracy and explainability on complex, multi-step claims. The limitation is that this approach is more computationally expensive and harder to adapt than simple classifier fine-tuning.

Overall, LLM-based and reasoning-based approaches improve explainability and, in some setups, accuracy, but they introduce additional system complexity, API costs, and compute requirements. For an MSc-scale project these methods are best treated as literature comparisons rather than as directly reproducible baselines.

---

## 2.4 Class Imbalance and Evaluation Metrics

Class imbalance is a common challenge in fake news detection datasets. Models trained on imbalanced data tend to favour the majority class, leading to poor performance on the minority class.

Henning et al. [13] conducted a comprehensive survey of class imbalance problems in NLP, reviewing methods including oversampling, undersampling, data augmentation, and loss function weighting. The survey found that class-weighted loss functions are often effective in practice for text classification tasks, as they directly adjust the contribution of each class during training without requiring data modification. The paper also discusses the choice of evaluation metric: accuracy is misleading under class imbalance, and Macro-F1 — which weights each class equally — is recommended as a more informative metric.

Johnson and Khoshgoftaar [14] surveyed class imbalance approaches specifically in the context of deep learning, covering a wider range of techniques including ensemble methods and cost-sensitive learning. They found that the optimal strategy depends on the degree of imbalance and the task, but that weighted loss functions are consistently competitive across scenarios.

In the context of fake news detection on LIAR, the binary mapping from six labels can produce a slight class imbalance depending on the mapping chosen. Models trained without addressing this imbalance tend to have higher REAL recall but lower FAKE recall. Since the real-world cost of missing a fake news item (false negative) is typically higher than wrongly flagging a real item (false positive), FAKE recall is an important supplementary metric alongside Macro-F1.

---

## 2.5 Robustness and Cross-Dataset Generalisation

Cross-dataset generalisation is one of the most important unsolved problems in fake news detection. A model that performs well on one dataset often drops significantly when tested on another.

Wang et al. [15] surveyed robustness research in NLP, covering domain shift, adversarial examples, and dataset bias. The survey found that models fine-tuned on a specific dataset often rely on dataset-specific patterns (shortcuts or spurious correlations) rather than general linguistic signals of truthfulness. This leads to brittle behaviour when the test distribution differs from training. In fake news detection, different datasets come from different sources, platforms, and annotation processes, which creates substantial distribution shifts between them.

Gururangan et al. [16] proposed Domain-Adaptive Pretraining (DAPT), a method in which a pre-trained language model is further pre-trained on domain-specific unlabelled text before task-specific fine-tuning. DAPT showed consistent improvements across a range of domain-specific tasks, suggesting that bridging the gap between the general pre-training distribution and the target task domain can improve both in-domain and cross-domain performance. This approach is directly relevant to cross-dataset fake news detection: by adapting the language model to the language style of a target dataset before fine-tuning, it may be possible to reduce the performance drop caused by domain shift.

Silva et al. [17] proposed a method that explicitly addresses cross-domain fake news detection by embracing domain differences rather than treating them as noise. Working on a combined dataset of PolitiFact (politics), GossipCop (entertainment), and CoAID (COVID-19), they empirically demonstrate that news from different domains differs significantly in both word usage and propagation patterns, and that single-domain detectors transfer poorly to unseen domains. Their framework maps each news record into two parallel embedding subspaces — one domain-specific, one cross-domain — and reports up to 7.55% F1 improvement over single-space baselines on the cross-domain dataset, with around 25% F1 improvement for rarely-appearing domains. The main limitation, from the perspective of a text-only project, is that the framework relies on Twitter propagation graphs, which are not part of LIAR and are no longer easy to re-collect.

Castelo et al. [18] took a different approach to the same problem, selecting a small set of features (such as readability and web-markup features) that are domain-invariant by construction, and showed that a classifier built on these features transfers more reliably across topical domains than a model trained on domain-specific lexical signals. The trade-off is the opposite of Silva et al. [17]: by discarding domain-specific information, Castelo et al. lose accuracy on individual in-domain test sets in exchange for stability across domains.

Han et al. [19] framed cross-domain fake news detection as a continual learning problem, in which a model sees a sequence of domains and must avoid catastrophic forgetting of earlier ones. They applied Elastic Weight Consolidation and Gradient Episodic Memory on top of a propagation-graph neural network, and showed that continual-learning regularisation reduces but does not eliminate the cross-domain performance drop. Their main limitations are the assumption that domain identity is known at training time and the assumption that domains arrive sequentially, neither of which holds in a typical real-world news stream.

Papageorgiou et al. [8] provided evidence from multi-dataset evaluation that performance varies substantially across different fake news datasets, reinforcing the conclusion that no current method achieves robust cross-dataset generalisation. While their evaluation is multi-dataset rather than strictly cross-domain (models are trained on each dataset separately), the observed variability in results supports the argument that cross-dataset generalisation remains an open problem.

---

## 2.6 Research Gap

The literature reviewed above shows that fake news detection has made substantial progress in several areas. Large benchmark datasets are now available [1, 2, 3]. Transformer-based models have improved in-domain performance considerably compared to feature-based approaches [6, 7]. More advanced systems have pushed performance further using LLM-based reasoning and explainability [9]. The importance of class imbalance and evaluation metric choice is well understood [13].

However, several gaps remain.

First, most existing studies evaluate models only within a single dataset. Performance on in-domain LIAR [1], for example, does not tell us how well the model would perform on FakeNewsNet [2] or MultiFC [3]. Systematic cross-dataset generalisation — training on one dataset and testing on another — remains underexplored for transformer-based models. Existing cross-domain work [17, 19, 18] is concentrated on social-media datasets with propagation graphs and does not directly address the case of short-statement, text-only datasets like LIAR.

Second, the impact of dataset-level differences — in label scheme, domain, and annotation style — on cross-dataset performance is not well understood. Even within the same family of models, different data sources lead to very different results, as shown by Papageorgiou et al. [8], and the propagation-pattern differences quantified by Silva et al. [17] confirm that the gap between datasets is substantial and statistically significant.

Third, advanced systems such as TELLER [9] and ARG [10] improve performance but require LLM API access and, in TELLER's case, expert-designed logical predicates, making them difficult to reproduce or adapt in constrained research environments. Pelrine et al. [11] further show that prompting LLMs directly does not consistently match fine-tuned smaller models. There is therefore a clear gap between high-performing, resource-intensive systems and accessible, reproducible baselines that can serve as reliable starting points for generalisation research.

Fourth, the relationship between class imbalance, evaluation metrics, and cross-domain transfer is not fully studied. When a model is transferred to a new dataset with a different class ratio, the effect on FAKE recall and Macro-F1 may differ from the in-domain case observed by Henning et al. [13], and this interaction has not been systematically reported.

These gaps motivate further work on reliable, reproducible in-domain baselines and systematic cross-dataset transfer for fake news detection. A particular need is to study training-efficient transformer-based methods that do not depend on external LLM APIs, while still reporting class-sensitive metrics such as Macro-F1 and FAKE recall.

## References

[1] W. Y. Wang. "Liar, Liar Pants on Fire": A New Benchmark Dataset for Fake News Detection. *Proceedings of the 55th Annual Meeting of the Association for Computational Linguistics (ACL)*, 2017.

[2] K. Shu, D. Mahudeswaran, S. Wang, D. Lee, and H. Liu. *FakeNewsNet: A Data Repository with News Content, Social Context and Spatiotemporal Information for Studying Fake News on Social Media*. *Big Data*, 2020. arXiv:1809.01286.

[3] I. Augenstein, C. Lioma, D. Wang, L. C. Lima, Casper Hansen, Christian Hansen, and J. G. Simonsen. *MultiFC: A Real-World Multi-Domain Dataset for Evidence-Based Fact Checking of Claims*. EMNLP 2019.

[4] H. Rashkin, E. Choi, J. Y. Jang, S. Volkova, and Y. Choi. *Truth of Varying Shades: Analyzing Language in Fake News and Political Fact-Checking*. *Proceedings of the 2017 Conference on Empirical Methods in Natural Language Processing (EMNLP)*, pages 2931-2937, 2017. DOI: 10.18653/v1/D17-1317.

[5] V. Pérez-Rosas, B. Kleinberg, A. Lefevre, and R. Mihalcea. *Automatic Detection of Fake News*. *Proceedings of the 27th International Conference on Computational Linguistics (COLING)*, pages 3391-3401, 2018.

[6] J. Devlin, M.-W. Chang, K. Lee, and K. Toutanova. *BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding*. NAACL 2019.

[7] Y. Liu, M. Ott, N. Goyal, J. Du, M. Joshi, D. Chen, O. Levy, M. Lewis, L. Zettlemoyer, and V. Stoyanov. *RoBERTa: A Robustly Optimized BERT Pretraining Approach*. arXiv:1907.11692, 2019.

[8] E. Papageorgiou, I. Varlamis, and C. Chronis. *Harnessing Large Language Models and Deep Neural Networks for Fake News Detection*. *Information*, 16(4):297, 2025. DOI: 10.3390/info16040297.

[9] H. Liu, W. Wang, H. Li, and H. Li. *TELLER: A Trustworthy Framework for Explainable, Generalizable and Controllable Fake News Detection*. *Findings of ACL 2024*, 2024. arXiv:2402.07776.

[10] B. Hu, Q. Sheng, J. Cao, Y. Shi, Y. Li, D. Wang, and P. Qi. *Bad Actor, Good Advisor: Exploring the Role of Large Language Models in Fake News Detection*. AAAI 2024. arXiv:2309.12247.

[11] K. Pelrine, A. Imouza, C. Thibault, M. Reksoprodjo, C. Gupta, J. Christoph, J.-F. Godbout, and R. Rabbany. *Towards Reliable Misinformation Mitigation: Generalization, Uncertainty, and GPT-4*. *Proceedings of the 2023 Conference on Empirical Methods in Natural Language Processing (EMNLP)*, pages 6399-6429, 2023. DOI: 10.18653/v1/2023.emnlp-main.395.

[12] L. Pan, X. Wu, X. Lu, A. T. Luu, W. Y. Wang, M.-Y. Kan, and P. Nakov. *Fact-Checking Complex Claims with Program-Guided Reasoning*. *Proceedings of the 61st Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers)*, pages 6981-7004, 2023. DOI: 10.18653/v1/2023.acl-long.386.

[13] S. Henning, W. Beluch, A. Fraser, and A. Friedrich. *A Survey of Methods for Addressing Class Imbalance in Deep-Learning Based Natural Language Processing*. *Proceedings of the 17th Conference of the European Chapter of the Association for Computational Linguistics (EACL)*, pages 523-540, 2023. DOI: 10.18653/v1/2023.eacl-main.38.

[14] J. M. Johnson and T. M. Khoshgoftaar. *Survey on Deep Learning with Class Imbalance*. *Journal of Big Data*, 6:27, 2019. DOI: 10.1186/s40537-019-0192-5.

[15] X. Wang, H. Wang, and D. Yang. *Measure and Improve Robustness in NLP Models: A Survey*. *Proceedings of the 2022 Conference of the North American Chapter of the Association for Computational Linguistics: Human Language Technologies (NAACL-HLT)*, pages 4569-4586, 2022.

[16] S. Gururangan, A. Marasovic, S. Swayamdipta, K. Lo, I. Beltagy, D. Downey, and N. A. Smith. *Don't Stop Pretraining: Adapt Language Models to Domains and Tasks*. ACL 2020.

[17] A. Silva, L. Luo, S. Karunasekera, and C. Leckie. *Embracing Domain Differences in Fake News: Cross-domain Fake News Detection using Multimodal Data*. AAAI 2021. arXiv:2102.06314.

[18] S. Castelo, T. Almeida, A. Elghafari, A. S. R. Santos, K. Pham, E. F. Nakamura, and J. Freire. *A Topic-Agnostic Approach for Identifying Fake News Pages*. *WWW '19 Companion: The World Wide Web Conference Companion*, pages 975-980, 2019. DOI: 10.1145/3308560.3316739.

[19] Y. Han, S. Karunasekera, and C. Leckie. *Graph Neural Networks with Continual Learning for Fake News Detection from Social Media*. arXiv:2007.03316, 2020.
