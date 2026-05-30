# Supervisor Reading Version: Chapters 2 and 3 with Updated Results Summary

Date: 2026-05-30

This version is intended for supervisor reading before the next meeting. It prioritizes Chapter 2 and Chapter 3, plus a concise summary of the updated rerun evidence. Chapter 6 has been updated internally, but it should not be the main material sent for close reading yet.

## What changed this week

- Re-ran the titles-only direct transfer baseline on five seeds.
- Re-ran the 10% and 20% intermediate fine-tuning settings on five seeds.
- Updated the integrated results table with the new five-seed means.
- Repositioned the 1000-row reasoning-atom experiment as a current-setup pilot.
- Added body-text explanations for target fraction, target training, intermediate fine-tuning, held-out test, seed, and pilot.

## Updated Results Summary

| Experiment | Protocol | Evidence | Accuracy | Macro-F1 | REAL recall | FAKE recall | Reading |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Titles-only direct transfer | LIAR train -> held-out FakeNewsNet title test | 5 seeds | 0.2725 +/- 0.0179 | 0.2364 +/- 0.0257 | 0.0377 +/- 0.0268 | 0.9842 +/- 0.0110 | Consistently weak; not a seed-42 accident. |
| Intermediate fine-tuning 10% | LIAR train -> stratified 10% FNN target-train titles -> held-out test | 5 seeds | 0.8083 +/- 0.0068 | 0.7035 +/- 0.0298 | 0.9305 +/- 0.0197 | 0.4379 +/- 0.0791 | Stable uplift over direct transfer; wording should say stratified, not 1:1 balanced. |
| Intermediate fine-tuning 20% | LIAR train -> stratified 20% FNN target-train titles -> held-out test | 5 seeds | 0.8243 +/- 0.0049 | 0.7463 +/- 0.0060 | 0.9167 +/- 0.0138 | 0.5444 +/- 0.0292 | Best absolute 5-seed target-fraction result so far; compare with 10% for efficiency. |
| 1000-row reasoning-atom pilot | LLM atoms with logistic decision layer | pilot | 0.5300 / 0.6000 | 0.4405 / 0.6000 | 0.1300 / 0.5900 | 0.9300 / 0.6100 | Current DeepSeek V4 Flash reasoning-atom setup shows limited performance in this pilot. |

The main result is now easier to state: titles-only direct transfer is consistently weak, while 10% and 20% intermediate fine-tuning both give stable improvements across seeds. The 10% result is the more data-efficient setting; the 20% result is currently the strongest absolute five-seed setting. The 1000-row atom result should be described only as a current DeepSeek V4 Flash reasoning-atom setup with limited performance in this pilot.

## Terminology Notes for Reader

| Term | Meaning in this dissertation |
| --- | --- |
| target fraction | The proportion of FakeNewsNet target-train titles used after the LIAR source model has been trained. In the current rerun, 10% means a stratified 10% sample from each target label, not a 1:1 balanced subset. |
| target training | The FakeNewsNet target-domain training subset used for adaptation. It is separate from validation and held-out test data. |
| intermediate fine-tuning | A two-stage training protocol: first fine-tune on LIAR, then continue fine-tuning on a small target-domain FakeNewsNet training subset before final held-out target testing. |
| held-out test | The final FakeNewsNet test split. It is not used for model training, checkpoint selection, threshold tuning, or explanation-driven adjustment. |
| seed | The random seed controlling model initialization, training order, and target-domain sampling/splitting. Multiple seeds are used to test whether a result is stable rather than accidental. |
| pilot | A small exploratory run used to test whether an idea is promising. A pilot can motivate discussion, but it should not be written as a strong conclusion without reruns or additional samples. |

# Chapter 2
## Literature Review

## 2.1 Fake News Detection Datasets and LIAR
Research in fake news detection has depended heavily on the availability of labelled datasets. Several benchmark datasets have been established, each with different scope, label schemes, and domain coverage.

Wang [1] introduced the LIAR dataset, one of the most widely used benchmarks in fake news detection research. LIAR was collected from PolitiFact.com and contains 12,836 labelled political statements. All statements are in English and were collected from PolitiFact between 2007 and 2016. Statements are typically short, with a median length of about 18 words; the dataset also provides speaker metadata and a context field that are not used in this dissertation. Each statement was assessed by expert fact-checkers and assigned one of six truthfulness labels: true, mostly-true, half-true, barely-true, false, and pants-on-fire. Metadata including speaker identity, political affiliation, and the context of the statement is also provided. The value of LIAR is significant: it offers a large-scale, naturally occurring political fake news corpus with fine-grained truthfulness labels. However, the six-class scheme presents a challenge for binary classification models, as the boundary between adjacent labels - particularly between half-true and barely-true - is ambiguous. This boundary ambiguity makes the task both harder and more realistic. Many subsequent studies map the six labels into a binary scheme (real / fake), following Wang's original suggestion.

Shu et al. [2] released FakeNewsNet, a dataset that goes beyond claim text to include social context information such as article content, news propagation paths, and user engagement signals on social media. FakeNewsNet covers two domains: political news (sourced from PolitiFact) and entertainment news (sourced from GossipCop). The multi-domain structure of FakeNewsNet makes it particularly suitable for studying cross-domain generalisation. However, the social context features require external data access and are not always easy to use in all experimental settings, especially when only claim text is available.

Augenstein et al. [3] presented MultiFC at EMNLP 2019, the largest publicly available dataset of naturally occurring fact-checked claims at the time. MultiFC aggregates claims from 26 English-language fact-checking websites, annotated by expert journalists, and includes associated evidence text. The dataset covers multiple domains - politics, science, and entertainment - and is notable for its diversity of sources and label schemes. MultiFC achieved a best Macro-F1 of only 49.2% in the original paper, reflecting how challenging cross-source veracity prediction is. The main limitation of MultiFC is the inconsistency in annotation standards across 26 different websites, which adds label noise and makes direct comparison between sources difficult.

These datasets vary considerably in domain, label scheme, and the kind of information they provide. This variation means that a model trained on LIAR may not perform well on FakeNewsNet or MultiFC, and vice versa. The mismatch between datasets - in terms of language style, topic focus, and annotation criteria - is a core motivation for studying cross-dataset generalisation.

Kuntur et al. [23] reviewed fake news detection from a dataset-centred perspective, arguing that dataset quality, label design, dataset diversity, and bias strongly shape model reliability. This is important for the present project because the main experimental problem is not only model selection, but also whether a model trained on one dataset remains meaningful when applied to another dataset. The limitation of this survey is that it provides broad dataset guidance rather than a direct LIAR-to-FakeNewsNet transfer experiment.

## 2.2 Traditional and Transformer-Based Fake News Detection
The field of fake news detection has evolved from hand-crafted feature approaches to pre-trained language model fine-tuning. Each stage has contributed to our understanding of how linguistic signals relate to truthfulness.

Early studies showed that language style itself carries veracity signals. Rashkin et al. [4] analysed the linguistic characteristics of fake news across different truthfulness levels, using the LIAR dataset. They found that deceptive statements tend to use more hedging language, stronger subjective sentiment, and fewer assertive phrases compared to truthful statements. This work demonstrated that even relatively simple linguistic features - captured by n-gram models - can be informative for veracity prediction. However, these models are highly domain-specific: features that distinguish true and false statements in political discourse may not transfer to entertainment or scientific domains.

Perez-Rosas et al. [5] further explored the use of linguistic features - including lexical, syntactic, and psycholinguistic features - for fake news detection. Their results confirmed that feature-based classifiers can achieve meaningful performance, but they also showed that performance drops significantly when models are tested on out-of-domain data. This finding highlighted the generalisation problem as a fundamental challenge for feature-based approaches.

A major shift occurred with the introduction of pre-trained language models. Devlin et al. [6] proposed BERT (Bidirectional Encoder Representations from Transformers), which learns contextual text representations through pre-training on large corpora using two objectives: masked language modelling (MLM) and next sentence prediction (NSP). BERT demonstrated strong performance across a wide range of NLP tasks through fine-tuning on task-specific labelled data. The contribution of BERT is foundational: it showed that deep bidirectional context modelling can capture subtle semantic nuances that earlier models missed.

Liu et al. [7] introduced RoBERTa (Robustly Optimized BERT Pretraining Approach), which revisited and improved BERT's pre-training by training on larger datasets, removing the NSP objective, and using dynamic masking. RoBERTa achieved state-of-the-art results on GLUE, RACE, and SQuAD benchmarks, outperforming BERT while using the same model architecture. RoBERTa has since become a strong baseline for text classification tasks, including fake news detection, due to its improved language understanding. The limitation of RoBERTa and similar models is that they are fine-tuned on a fixed training domain and may not generalise well when the test distribution differs significantly.

Papageorgiou et al. [8] conducted a large-scale comparison of current methods across multiple fake news datasets, including LIAR and FakeNewsNet. The study compared traditional models, BERT-based classifiers, and LLM-based approaches, finding that performance varies substantially across datasets. This multi-dataset evaluation highlights that no single model achieves consistently strong results across all benchmarks. Importantly, this study evaluates each dataset separately - training and testing on the same dataset - rather than testing strict cross-dataset transfer. The distinction matters: multi-dataset evaluation does not directly measure a model's ability to transfer from one domain to another.

**Table 2.1. Summary of prior literature on fake news classification and dataset benchmarks.**

| Study | Model(s) Used | Dataset(s) | Reported Metric(s) | Key Findings and Limitations |
| --- | --- | --- | --- | --- |
| Wang [1] | SVM, Logistic Regression | LIAR (6-class) | ~27.7% Accuracy | Baseline paper; metadata improves accuracy slightly but text-only remains low. |
| Rashkin et al. [4] | MaxEnt, Naive Bayes, LSTM | LIAR (binary) | ~62.0% Macro-F1 | Found stylistic and sentiment patterns; highly specific to political domain. |
| Perez-Rosas [5] | SVM with linguistic and lexical features | Custom, FakeNewsNet | ~70.0%-80.0% Accuracy | Strong in-domain performance but 15-20 point drops out of domain. |
| Devlin et al. [6] | BERT-Base / Large | GLUE benchmarks | - | Established bidirectional representation fine-tuning; no transfer tested. |
| Liu et al. [7] | RoBERTa-Base | GLUE, SQuAD | - | Optimised BERT pre-training; transfer under distribution shift not evaluated. |
| Papageorgiou [8] | BERT, traditional models, LLMs | LIAR, FakeNewsNet | ~65.0%-68.0% Accuracy | Evaluated multiple datasets independently; did not run strict zero-shot transfer. |

## 2.3 LLM and Reasoning-Based Fake News Detection
Recent advances in large language models have opened new directions for fake news detection. Rather than relying solely on fine-tuned classifiers, a growing body of research explores the use of LLMs for generating explanations, structured reasoning, and logic-guided predictions.

Liu et al. [9] proposed TELLER, an LLM-based framework published at Findings of ACL 2024. TELLER addresses three limitations of existing approaches: the lack of explainability in neural classifiers, poor generalisation across domains, and the risks of integrating LLMs without control mechanisms. The framework operates through two systems: a cognition system, which uses human-designed logical predicates to prompt an LLM and generate structured logic atoms from the input claim; and a decision system, which learns generalizable logic rules to aggregate these atoms and produce a prediction. On the LIAR binary task, TELLER reports an accuracy of 0.6773 and Macro-F1 of 0.6697, which is higher than standard BERT and RoBERTa fine-tuned baselines. The key limitation of TELLER is its dependency on the OpenAI API for the logic atom generation step, which introduces rate limits and dependency on an external service. While open-source LLMs can run locally and eliminate API costs, they introduce substantial local compute and hardware requirements. The logic predicates also require human expertise to design, making the system less straightforward to reproduce or adapt.

Hu et al. [10] examined the dual role of LLMs in the fake news ecosystem - as a potential tool for generating disinformation (the "bad actor" role) and as a tool for detecting it (the "good advisor" role). Their empirical study shows that GPT-3.5 prompted directly to predict fake or real news consistently underperforms a fine-tuned BERT on both Chinese and English benchmarks (Weibo21 and GossipCop), but that LLM-generated rationales - defined as natural-language explanations produced by an LLM for each input claim - when used as a side input to a small fine-tuned model rather than as the predictor, produce a stronger system than either model alone. Their proposed Adaptive Rationale Guidance (ARG) network frames the LLM as an advisor rather than a detector. The main limitation is that ARG still requires LLM access during training; the choice between proprietary APIs and locally hosted open-source LLMs determines the practical reproducibility cost.

Pelrine et al. [11] provided one of the first systematic comparisons of LLM prompting strategies for fake news detection across multiple datasets. Their results showed that LLM-only baselines, even with carefully designed prompts, do not consistently match fine-tuned smaller models on standard benchmarks. This finding is consistent with Hu et al. [10] and supports the more cautious view that LLMs alone are not yet a drop-in replacement for fine-tuned classifiers in this task. The limitation of this work is that it does not propose a new system, but its diagnostic value is clear.

Pan et al. [12] proposed a program-guided reasoning approach for fact-checking complex claims, presented at ACL 2023. The system decomposes a claim into Python-like programs that call sub-tasks (such as verifying a date or comparing numbers), and aggregates the sub-task outputs into a final verdict. This method demonstrates that structured reasoning can improve both accuracy and explainability on complex, multi-step claims. The limitation is that this approach is more computationally expensive and harder to adapt than classifier fine-tuning.

Overall, LLM-based and reasoning-based approaches improve explainability and, in some setups, accuracy, but they introduce additional system complexity and compute requirements. Reproducing TELLER was outside the scope of this dissertation given the time and equipment constraints of this project, and would have required either commercial API access or setting up a local open-source LLM with predicate prompting; this was not pursued.

## 2.4 Class Imbalance and Evaluation Metrics
Class imbalance is a common challenge in fake news detection datasets. Models trained on imbalanced data tend to favour the majority class, leading to poor performance on the minority class.

Henning et al. [13] conducted a comprehensive survey of class imbalance problems in NLP, reviewing methods including oversampling, undersampling, data augmentation, and loss function weighting. The survey found that class-weighted loss functions are often effective in practice for text classification tasks, as they directly adjust the contribution of each class during training without requiring data modification. The paper also discusses the choice of evaluation metric: accuracy is misleading under class imbalance, and Macro-F1 - which weights each class equally - is recommended as a more informative metric.

Johnson and Khoshgoftaar [14] surveyed class imbalance approaches specifically in the context of deep learning, covering a wider range of techniques including ensemble methods and cost-sensitive learning. They found that the optimal strategy depends on the degree of imbalance and the task, but that weighted loss functions are consistently competitive across scenarios.

In the context of fake news detection on LIAR, the binary mapping from six labels can produce a slight class imbalance depending on the mapping chosen. Models trained without addressing this imbalance tend to have higher REAL recall but lower FAKE recall. Since the real-world cost of missing a fake news item (false negative) is typically higher than wrongly flagging a real item (false positive), FAKE recall is an important supplementary metric alongside Macro-F1.

## 2.5 Robustness and Cross-Dataset Generalisation
Cross-dataset generalisation is one of the most important unsolved problems in fake news detection. A model that performs well on one dataset often drops significantly when tested on another.

Wang et al. [15] surveyed robustness research in NLP, covering domain shift, adversarial examples, and dataset bias. The survey found that models fine-tuned on a specific dataset often rely on dataset-specific patterns (shortcuts or spurious correlations) rather than general linguistic signals of truthfulness. This leads to brittle behaviour when the test distribution differs from training. In fake news detection, different datasets come from different sources, platforms, and annotation processes, which creates substantial distribution shifts between them.

Gururangan et al. [16] proposed Domain-Adaptive Pretraining (DAPT), a method in which a pre-trained language model is further pre-trained on domain-specific unlabelled text before task-specific fine-tuning. DAPT showed consistent improvements across a range of domain-specific tasks, suggesting that bridging the gap between the general pre-training distribution and the target task domain can improve both in-domain and cross-domain performance. This approach is directly relevant to cross-dataset fake news detection: by adapting the language model to the language style of a target dataset before fine-tuning, it may be possible to reduce the performance drop caused by domain shift.

Silva et al. [17] proposed a method that explicitly addresses cross-domain fake news detection by embracing domain differences rather than treating them as noise. Working on a combined dataset of PolitiFact (politics), GossipCop (entertainment), and CoAID (COVID-19), they empirically demonstrate that news from different domains differs significantly in both word usage and propagation patterns, and that single-domain detectors transfer poorly to unseen domains. Their framework maps each news record into two parallel embedding subspaces - one domain-specific, one cross-domain - and reports up to 7.55% F1 improvement over single-space baselines on the cross-domain dataset, with around 25% F1 improvement for rarely-appearing domains. The main limitation, from the perspective of a text-only project, is that the framework relies on Twitter propagation graphs, which are not part of LIAR and are no longer easy to re-collect.

Castelo et al. [18] took a different approach to the same problem, selecting a small set of features (such as readability and web-markup features) that are domain-invariant by construction, and showed that a classifier built on these features transfers more reliably across topical domains than a model trained on domain-specific lexical signals. The trade-off is the opposite of Silva et al. [17]: by discarding domain-specific information, Castelo et al. lose accuracy on individual in-domain test sets in exchange for stability across domains.

Han et al. [19] framed cross-domain fake news detection as a continual learning problem, in which a model sees a sequence of domains and must avoid catastrophic forgetting of earlier ones. They applied Elastic Weight Consolidation and Gradient Episodic Memory on top of a propagation-graph neural network, and showed that continual-learning regularisation reduces but does not eliminate the cross-domain performance drop. Their main limitations are the assumption that domain identity is known at training time and the assumption that domains arrive sequentially, neither of which holds in a typical real-world news stream.

Papageorgiou et al. [8] provided evidence from multi-dataset evaluation that performance varies substantially across different fake news datasets, reinforcing the conclusion that no current method achieves robust cross-dataset generalisation. While their evaluation is multi-dataset rather than strictly cross-domain (models are trained on each dataset separately), the observed variability in results supports the argument that cross-dataset generalisation remains an open problem.

Wei et al. [20] directly addressed cross-domain fake news detection for unseen domains using dual-granularity adversarial training. Their method models both document-level and entity-level representations to reduce domain-specific bias, and they argue that entity-label relationships can change across domains. This paper is highly relevant because it treats cross-domain fake news detection as a central problem rather than a secondary evaluation. Its limitation for the present dissertation is that it proposes a specialised adversarial architecture, while the current project focuses on reproducible baseline transfer.

Liguori et al. [21] proposed MERMAID, a mixture-of-experts approach for cross-domain fake news detection. Their formulation is close to zero-shot domain generalisation: models learn from known domains and classify examples from unseen domains. This supports the importance of the LIAR-to-FakeNewsNet setting in this dissertation. However, MERMAID is a more complex ensemble framework than the simple BERT and RoBERTa baselines used here, so it is best treated as future-work literature rather than as a direct baseline.

Kishi et al. [22] studied fake news detection under dataset bias and explicitly distinguished in-dataset and cross-dataset evaluation. Their results show that detection performance depends strongly on dataset-specific biases and annotation policies. This directly supports the interpretation of the current transfer results: a model may perform acceptably on LIAR but fail on FakeNewsNet because the datasets encode different content distributions and labelling assumptions.

Dodge et al. [24] showed that fine-tuning pretrained language models can vary substantially across random seeds, including weight initialisation and training data order. This supports the five-seed evaluation protocol used in this dissertation. A single fine-tuned BERT or RoBERTa run may give an unstable view of model quality, so mean and standard deviation provide a more reliable comparison.

Swayamdipta et al. [25] introduced dataset cartography, using training dynamics to identify easy-to-learn, hard-to-learn, and ambiguous examples. Although not specific to fake news detection, this work helps interpret the LIAR error analysis: label-boundary cases such as half-true and barely-true claims can be understood as ambiguous examples rather than simple model mistakes.

## 2.6 Research Gap
The literature reviewed above shows that fake news detection has made substantial progress in several areas. Large benchmark datasets are now available [1, 2, 3]. Transformer-based models have improved in-domain performance considerably compared to feature-based approaches [6, 7]. More advanced systems have pushed performance further using LLM-based reasoning and explainability [9]. The importance of class imbalance and evaluation metric choice is well understood [13].

However, several gaps remain.
First, most existing studies evaluate models only within a single dataset. Performance on in-domain LIAR [1], for example, does not tell us how well the model would perform on FakeNewsNet [2] or MultiFC [3]. Systematic cross-dataset generalisation - training on one dataset and testing on another - remains underexplored for transformer-based models. Existing cross-domain work [17, 19, 18] is concentrated on social-media datasets with propagation graphs and does not directly address the case of short-statement, text-only datasets like LIAR.

Second, the impact of dataset-level differences - in label scheme, domain, and annotation style - on cross-dataset performance is not well understood. Recent work has started to address cross-domain fake news detection more directly [20, 21, 22], but these studies often use specialised architectures or multi-domain training assumptions. There is a distinct gap in literature regarding: (1) how LIAR-trained classifiers transfer to class-imbalanced targets like FakeNewsNet minimal titles under zero-shot transfer, (2) the absence of a trivial majority-class baseline as a sanity check for transfer quality, and (3) the role of class-weighted training in mitigating or exacerbating transfer performance drops. This leaves space for a controlled, reproducible baseline study that makes the transfer failure visible and isolates the effects of loss weighting before adding complex domain adaptation layers.

Third, advanced systems such as TELLER [9] and ARG [10] improve performance but require LLM API access and, in TELLER's case, expert-designed logical predicates, making them difficult to reproduce or adapt in constrained research environments. Pelrine et al. [11] further show that prompting LLMs directly does not consistently match fine-tuned smaller models. There is therefore a clear gap between high-performing, resource-intensive systems and accessible, reproducible baselines that can serve as reliable starting points for generalisation research.

Fourth, the relationship between class imbalance, evaluation metrics, and cross-domain transfer is not fully studied. When a model is transferred to a new dataset with a different class ratio, the effect on FAKE recall and Macro-F1 may differ from the in-domain case observed by Henning et al. [13], and this interaction has not been systematically reported.

Fifth, seed variance and dataset ambiguity are often underreported in fake news detection experiments. Dodge et al. [24] show why multiple fine-tuning seeds are important for pretrained language models, while Swayamdipta et al. [25] show that ambiguous and hard-to-learn examples can reveal dataset quality issues. These points are directly relevant to LIAR, where several binary errors occur near the boundary between half-true and barely-true claims.

These gaps motivate further work on reliable, reproducible in-domain baselines and systematic cross-dataset transfer for fake news detection. A particular need is to study training-efficient transformer-based methods that do not depend on external LLM APIs, while still reporting class-sensitive metrics such as Macro-F1 and FAKE recall.

# Chapter 3
## Methodology

## 3.1 Overview
This dissertation uses a staged experimental design. The first stage builds reliable in-domain baselines on the LIAR dataset. The second stage analyses whether class-weighted training changes model behaviour, especially for the FAKE class. The third stage measures strict titles-only direct transfer, where models trained on LIAR statements are evaluated on FakeNewsNet titles without target-domain adaptation. The fourth stage introduces limited intermediate fine-tuning on a small FakeNewsNet target-training subset to test whether a modest amount of target-domain supervision can reduce the direct-transfer failure.

The design keeps the project controlled and reproducible. All main models use the same binary label mapping, the same LIAR train, validation, and test splits, and the same statement field as input. This makes the comparison between TF-IDF, BERT, weighted BERT, and weighted RoBERTa controlled rather than changing several variables at the same time.

The direct-transfer setting is deliberately strict: no FakeNewsNet examples are used for source-model training, threshold selection, or checkpoint selection. The intermediate fine-tuning setting is separate from this zero-shot baseline. It uses a clearly defined FakeNewsNet target-training subset after LIAR training, while keeping the held-out FakeNewsNet test split untouched for final evaluation.

## 3.2 Datasets
### 3.2.1 LIAR Dataset
The main source dataset is LIAR. It contains short political statements collected from PolitiFact and labelled by fact-checkers. The original dataset has six labels: true, mostly-true, half-true, barely-true, false, and pants-on-fire. These labels are useful because they capture degrees of truthfulness, but they also create difficult boundary cases.

This project keeps the official LIAR split structure. The dataset split and label distributions after binary mapping are summarized in Table 3.2.

**Table 3.2. Dataset splits and label distributions for LIAR and FakeNewsNet.**

| Dataset | Split | REAL Count (%) | FAKE Count (%) | Total Rows |
| --- | --- | ---: | ---: | ---: |
| LIAR (Source) | Train | 5,752 (56.17%) | 4,488 (43.83%) | 10,240 |
| LIAR (Source) | Validation | 668 (52.02%) | 616 (47.98%) | 1,284 |
| LIAR (Source) | Test | 714 (56.35%) | 553 (43.65%) | 1,267 |
| FakeNewsNet (Target) | PolitiFact Titles | 624 (59.09%) | 432 (40.91%) | 1,056 |
| FakeNewsNet (Target) | GossipCop Titles | 16,817 (75.96%) | 5,323 (24.04%) | 22,140 |
| FakeNewsNet (Target) | Combined Titles | 17,441 (75.19%) | 5,755 (24.81%) | 23,196 |

The input field is the statement text. This is the same field used by the original TF-IDF baseline and by all transformer baselines in this project. Other LIAR metadata fields are not used in the main reported baseline results, because the dissertation first aims to compare text-only models under a controlled setting.

### 3.2.2 FakeNewsNet Minimal Titles
FakeNewsNet minimal is used as the first target dataset for cross-dataset evaluation. The processed file used in this project is data/fakenewsnet_minimal/processed/fakenewsnet_minimal_titles.csv. It contains title text and binary labels from the minimal release rather than full article bodies.

After cleaning, the target set contains 23,196 titles. The combined target set is much larger and more imbalanced than LIAR, as detailed in Table 3.2.

Because FakeNewsNet minimal provides titles rather than full article content, the transfer experiment should be interpreted carefully. The experiment is LIAR statement to FakeNewsNet title transfer, not full-article fake news detection. This limitation is important, but the experiment still tests whether short-text patterns learned from LIAR transfer to a different dataset family.

## 3.3 Binary Label Mapping
The original LIAR six-way labels are mapped to a binary REAL versus FAKE task. The mapping follows the existing project baseline and is kept fixed for all LIAR models. The purpose is to make the task consistent with common binary fake news detection settings and compatible with the binary labels in FakeNewsNet minimal.

**Table 3.1. Binary label mapping.**

| Binary label | Original LIAR labels |
| --- | --- |
| REAL | true, mostly-true, half-true |
| FAKE | barely-true, false, pants-on-fire |

## 3.4 Experimental Terminology for Transfer and Fine-Tuning

This dissertation uses several experimental terms in a narrow and reproducible way. The target fraction is the proportion of FakeNewsNet target-train titles used after the LIAR-trained source model has already been trained. For example, the 10% condition uses 1,484 target-train titles per seed. The current code samples this subset stratified by label, so "10%" should be read as a stratified target fraction rather than a 1:1 balanced training subset.

Target training refers only to the FakeNewsNet training subset used for adaptation. It is not the held-out target test set. Intermediate fine-tuning means that the model is first fine-tuned on LIAR and then further fine-tuned on this small FakeNewsNet target-training subset. The held-out test is the final FakeNewsNet test split; it is kept separate from training, validation, checkpoint selection, and threshold tuning.

A seed is the random seed controlling initialization, training order, and target-domain sampling. Reporting several seeds is important because fine-tuned transformer models can vary across random runs. A pilot is a small exploratory experiment, such as the 1000-row reasoning-atom run, that can guide discussion but should not be presented as a strong conclusion unless it is repeated or enlarged.

## 3.5 Model Configuration
For the TF-IDF baseline, the statement text is converted into sparse lexical features and classified using Logistic Regression. This gives a simple and deterministic reference point. It is important because any transformer improvement should be judged against a transparent baseline, not only against other neural models.

For the transformer baselines, the project uses bert-base-uncased and roberta-base from HuggingFace Transformers. Each model is fine-tuned as a sequence classifier on the binary LIAR task. Weighted BERT and weighted RoBERTa keep the same architecture but replace the standard cross-entropy loss with class-weighted cross-entropy during training.
