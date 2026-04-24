# Literature Review Draft

## 1. Fake News Detection Datasets and LIAR

Fake news detection usually needs datasets to train and test models. Different datasets can contain different types of text. Some datasets contain full news articles, while others contain short sentences, social media content, or political statements. Because of this, a model that works well on one dataset may not work equally well on another dataset.

LIAR is a commonly used dataset in fake news detection. It was introduced by Wang (2017), and its content mainly comes from political statements on PolitiFact. The text in LIAR is usually short. It is not full news articles, but one sentence or a short statement.

This makes LIAR difficult. Because the statements are short, the model has limited information to use. In many cases, judging whether a statement is true or false also requires extra political background or factual knowledge. However, this background information is not always included in the statement itself.

LIAR was originally a six-class dataset. This means that each statement has one of six different truthfulness labels. Many later studies simplify this into binary classification, where the labels are grouped into real and fake. Binary classification makes results easier to compare, but it also creates problems. Some labels are originally in the middle and are not clearly true or clearly false. If these labels are forced into either real or fake, the model can easily become confused.

Therefore, LIAR is a useful dataset because it represents the short political statement setting. However, it is also not an easy dataset, because the text is short, the label boundary is unclear, and many statements require background knowledge.

## 2. Transformer-Based Fake News Detection

Early fake news detection methods often used traditional machine learning models, such as Logistic Regression, or word-frequency features such as TF-IDF. These methods are simple and useful as baselines. However, they mainly look at the words themselves and do not understand context very well.

Later, Transformer models became very common in NLP. BERT is one important model in this direction. It was introduced by Devlin et al. (2019). BERT can understand the meaning of words and sentences based on context, so it is often used in text classification tasks.

In fake news detection, models such as BERT are usually stronger than TF-IDF. This is because BERT does not only check whether a word appears. It can also look at the relationship between words in a sentence.

However, BERT cannot fully solve the fake news detection problem. The reason is that judging whether a statement is true or false is not only about understanding the text. It also requires knowing the real-world facts. For example, a model may understand the meaning of a political statement, but it may not know whether the statement is actually correct in the real world.

Therefore, Transformer models can improve fake news detection, but they still have limitations. This is especially true for short statement datasets such as LIAR, where the model may not have enough information to make an accurate decision.

Some recent studies have started to use more complex methods, such as large language models, reasoning methods, or graph-based methods. These methods do not only do simple classification. They try to add more explanation or reasoning ability. For example, TELLER is a more complex fake news detection framework, not a normal BERT or RoBERTa classifier. Therefore, it can be used as an advanced method from the literature, but it should not be directly compared as the same type of model as a normal BERT baseline.

## 3. Class Imbalance and Evaluation Metrics

In fake news detection, looking only at accuracy is sometimes not enough. A model may have acceptable overall accuracy, but it may mainly classify real examples well and perform poorly on fake examples.

This is important in fake news detection because one key goal of the task is to find fake information. If a model misses many fake examples, then even if its accuracy is not low, the model may still not be very useful.

Therefore, researchers often look at other metrics, such as macro-F1 and recall for each class. Macro-F1 gives more balanced attention to different classes. Recall shows whether the model misses many examples from a specific class.

Class imbalance is also a common problem. Some classes may have more examples, or they may be easier to learn. Henning et al. (2023) summarised methods for dealing with class imbalance in NLP, such as resampling, data augmentation, and changing the loss function.

Weighted loss is one simple method. It means that mistakes on some classes are treated as more important during training. In this way, the model pays more attention to classes that are harder to learn or more important.

However, weighted loss can also create a trade-off. For example, the model may catch more fake examples, but it may also wrongly classify some real examples as fake. Therefore, when evaluating a model, it is not enough to look at only one overall score. It is also important to look at the performance for each class.

## 4. Robustness and Cross-Dataset Generalisation

A model that performs well on one dataset may not perform well on another dataset. This is a generalisation problem. Wang, Wang, and Yang (2022) connect this problem with robustness. They point out that a model may only learn special patterns from one dataset, instead of learning general rules that work in other datasets.

This problem is very clear in fake news detection. Different fake news datasets can be very different. For example, some datasets contain political statements, some contain full news articles, and some contain social media content. Their topics, text lengths, labels, and sources can all be different.

Therefore, testing a model on only one dataset is not enough. Models should also be tested across different datasets to see whether they can adapt to new data.

There are two related ideas that need to be separated. The first is multi-dataset evaluation. This means testing a model separately on several datasets. The second is strict cross-dataset transfer. This means training a model on one dataset and testing it on another dataset. The second one is a stronger way to test whether the model really has generalisation ability.

Some recent fake news detection papers use multiple datasets. This shows that the field is no longer only focused on a single dataset. However, using multiple datasets does not always mean doing real cross-dataset transfer. This difference needs to be explained clearly in later research.

## 5. Research Gap

Previous research has already done a lot of work on fake news detection, especially using Transformer models and more complex reasoning methods. However, some problems are still not fully solved.

First, many studies still mainly focus on results inside one dataset. This can show how well a model performs on that dataset, but it cannot show whether the model will still work well on another dataset.

Second, many studies mainly report overall performance, such as accuracy or F1-score. However, in fake news detection, it is also important to look more carefully at each class, especially whether the model can correctly find fake examples.

Third, some papers use multiple datasets, but they do not always do real train-on-one-dataset and test-on-another experiments. Therefore, the difference between multi-dataset evaluation and strict cross-dataset transfer needs to be clearer.

Overall, fake news detection still needs more research on three points: whether models can generalise across datasets, whether model performance is balanced across classes, and how to design clearer cross-dataset testing.
