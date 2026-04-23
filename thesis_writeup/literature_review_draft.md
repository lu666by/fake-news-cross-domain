# Literature Review Draft

## 1. Introduction

Fake news detection has become an important task in natural language processing because misleading or false information can spread quickly online and influence public opinion. Early work often focused on in-domain classification, where a model is trained and tested on the same dataset. However, strong in-domain results do not necessarily mean that a model will generalise well to new datasets or new domains. This is especially important in fake news detection, where datasets often differ in writing style, label design, source type, and annotation criteria.

This dissertation studies fake news detection with a particular focus on **cross-dataset generalisation**. Before testing cross-dataset performance, it is necessary to establish strong and clearly analysed in-domain baselines. For this reason, the current stage of the project focuses on the **LIAR** dataset and compares sparse and transformer-based baselines under a binary classification setting.

## 2. LIAR as a benchmark dataset

A central dataset in this project is **LIAR**, introduced by Wang (2017). LIAR is a benchmark dataset of short political statements collected from PolitiFact. The original dataset uses a fine-grained **6-way label scale**, which makes it useful as a benchmark for statement-level fact classification. The dataset is important because it provides short, claim-like political text rather than longer news articles, which makes the classification problem particularly challenging.

In the current project, LIAR is converted into a **binary setup**. The labels `true`, `mostly-true`, and `half-true` are mapped to **REAL**, while `barely-true`, `false`, and `pants-fire` are mapped to **FAKE**. This binary setting is more suitable for the current baseline stage, but it also creates a narrow semantic boundary between the two classes. This is one reason why the task remains difficult even when stronger transformer models are used.

The LIAR paper is therefore useful mainly in two ways. First, it provides the dataset background and motivates the use of short political claims as a benchmark. Second, it helps explain why the current project should be careful when comparing results, because the original LIAR setting is not directly the same as the current binary setup.

## 3. Transformer baselines for fake news detection

Transformer-based language models have become standard baselines in many NLP classification tasks. A key model is **BERT** (Devlin et al., 2019), which introduced bidirectional pre-training for deep contextual language representation. BERT is highly relevant to this dissertation because it provides a strong and widely accepted neural baseline for text classification.

For fake news detection, transformer models are attractive because they can capture contextual patterns beyond sparse lexical features such as TF-IDF. However, stronger contextual encoding does not automatically solve all difficulties in misinformation detection. In short-claim datasets such as LIAR, many statements are brief, ambiguous, and highly dependent on political or factual context that is not fully available in the text itself. As a result, transformer models often improve performance, but the gain is usually moderate rather than dramatic.

A more recent study by Papageorgiou et al. (2025) is also relevant because it evaluates modern fake news detection approaches across multiple datasets, including LIAR. That paper is useful for showing that transformer-based models are the correct model family for current fake news detection work. At the same time, it should be described carefully: it uses **multiple datasets**, but it does **not** use the same strict train-on-one-dataset and test-on-another-dataset setup planned later in this dissertation. It is therefore most useful as support for **multi-dataset evaluation** and generalisability discussion rather than as a direct example of strict cross-dataset transfer.

## 4. Class imbalance and weighted training

Another important issue in fake news detection is **class imbalance**. Even when the class counts are not extremely skewed, models may still show uneven behaviour across classes. In the current LIAR binary setup, one of the main weaknesses of early baselines is that the models tend to perform better on the **REAL** class than on the **FAKE** class.

This issue is consistent with the broader NLP literature on class imbalance. Henning et al. (2023) show that class imbalance remains a major challenge in deep-learning-based NLP, including in the transformer era. Their survey explains that common practical approaches include re-sampling, data augmentation, and changing the loss function. Among these, **weighted loss** is especially relevant to this dissertation because it is a simple and interpretable way to increase minority-class sensitivity.

The survey is also useful from an evaluation perspective. It argues that overall accuracy alone is often misleading in imbalanced settings, and that researchers should report **per-class statistics** and **macro-level metrics**. This is directly relevant here because the current LIAR experiments show that a model can improve overall performance while still handling the FAKE class differently from the REAL class. For this reason, the project uses **macro-F1** and class-wise recall, especially **FAKE recall**, as important evaluation indicators alongside accuracy.

## 5. Robustness and cross-dataset generalisation

The longer-term motivation of this dissertation is not only to improve in-domain scores, but also to understand **robustness under dataset shift**. Wang, Wang, and Yang (2022) provide a useful framework for this. Their survey explains that robustness in NLP is closely related to how much model performance degrades when the test distribution differs from the training distribution. In other words, a model can achieve good in-domain results while still relying on dataset-specific shortcuts that do not transfer well.

This point is especially relevant to fake news detection. Different datasets may vary in topic, label design, text length, and source characteristics. As a result, a model trained on one benchmark may not generalise well to another. Wang et al. (2022) therefore support the use of **cross-dataset evaluation** as a practical way to test robustness to natural distribution shift.

A related methodological direction comes from Gururangan et al. (2020), who argue that pre-trained language models can benefit from further adaptation to specific domains or tasks. Their work on domain-adaptive pre-training (DAPT) and task-adaptive pre-training (TAPT) is relevant because it provides a possible lightweight adaptation strategy for later stages of this dissertation. Even if such adaptation is not the immediate next step, it offers a theoretically grounded option for improving cross-dataset transfer once the baseline comparison is complete.

## 6. Positioning of the current project

Based on this literature, the current dissertation can be positioned as follows. First, LIAR is used as a well-established benchmark for short political claims, but in a binary setting that is better aligned with the current baseline stage. Second, transformer models such as BERT provide a strong neural baseline, while class imbalance literature justifies the use of weighted training and the reporting of macro-F1 and per-class recall. Third, robustness and domain-shift literature provide the broader motivation for moving beyond in-domain performance toward cross-dataset evaluation.

The current project therefore follows a staged logic. It first establishes a clear **LIAR in-domain baseline line** using sparse and transformer methods. It then analyses class-balance trade-offs and error patterns in detail. After that, it will move toward **cross-dataset / cross-domain** experiments, where the main question is no longer only whether one model scores slightly higher than another, but whether the learned representations transfer beyond the original benchmark.

## 7. Summary

The literature suggests four main points that guide this dissertation.

First, LIAR is a useful but challenging benchmark because it contains short political claims and was originally designed as a fine-grained fact classification dataset. Second, transformer baselines are stronger than sparse baselines, but the expected improvement is meaningful rather than dramatic. Third, class imbalance remains important even in transformer-based NLP, which justifies weighted training and class-sensitive evaluation. Fourth, robust fake news detection should not be judged only by in-domain performance, because cross-dataset generalisation is a central part of real-world usefulness.

These points provide the foundation for the current project structure: establish strong LIAR baselines first, analyse their behaviour carefully, and then move toward cross-dataset generalisation.
