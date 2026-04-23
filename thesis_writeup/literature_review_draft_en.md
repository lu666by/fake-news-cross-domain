# Literature Review Draft

## 1. Dataset background: LIAR

At the current stage of this project, the main dataset is **LIAR**, which is used to build the in-domain fake news detection baseline. LIAR was introduced by Wang (2017) and is based on political statements collected from PolitiFact. Unlike standard news classification datasets, LIAR is made up of short political statements rather than full news articles. Because of this, each example contains relatively limited lexical and contextual information, which makes the task more challenging.

The original LIAR dataset uses a **6-class label scheme**. In this project, I convert it into a **binary classification** setting, because this is more suitable for the current baseline stage. Specifically, `true`, `mostly-true`, and `half-true` are mapped to **REAL**, while `barely-true`, `false`, and `pants-fire` are mapped to **FAKE**. This makes the baseline comparison cleaner, but it also creates a narrower boundary between the two classes. Labels such as `half-true` and `barely-true`, which are already close in meaning, become especially difficult to separate after this binary mapping.

For this reason, I think LIAR is a suitable dataset for the current stage of the dissertation. It is a well-known and established benchmark, but it is also difficult enough to reveal the practical limits of both sparse and transformer-based baselines in a short political statement setting.

## 2. Model and method justification: BERT and weighted loss

One core model in the current baseline line is **BERT** (Devlin et al., 2019). BERT has become one of the standard transformer baselines for text classification, so it is a natural model choice for this project. In my case, BERT mainly serves as a stronger neural baseline than TF-IDF, allowing me to test whether contextual representations can help the model better judge the truthfulness of short statements.

However, the current experiments show that switching to a stronger transformer backbone does not automatically solve the problem. Many LIAR statements are short, ambiguous, and dependent on factual or political context that is not fully present in the text itself. Because of this, the improvement from TF-IDF to BERT is real, but it is better described as meaningful rather than dramatic.

Another important issue is **class imbalance** and, more importantly, class-sensitive model behaviour. In the current LIAR binary setup, one repeated pattern is that models tend to perform better on the **REAL** class than on the **FAKE** class. This is why I introduced **weighted loss**. The class imbalance literature supports this choice, because weighted loss is a direct way to make the model pay more attention to one type of error during training. In this project, its purpose is not only to improve accuracy, but also to make the model more sensitive to the **FAKE** class.

This also affects how the models should be evaluated. If I look only at accuracy, it is easy to hide important class-level differences. For this reason, the project also places clear emphasis on **macro-F1** and **FAKE recall**. In particular, FAKE recall is useful because it shows whether weighted training is actually changing model behaviour in the intended direction, rather than only causing a small change in the overall score.

## 3. Robustness and cross-dataset motivation

The longer-term goal of this dissertation is not only to improve in-domain performance on LIAR, but also to study **cross-dataset / cross-domain generalisation**. This is closely connected to the robustness literature. Wang, Wang, and Yang (2022) argue that strong performance under the same training and test distribution does not necessarily mean that a model is robust. In many cases, a model may simply learn dataset-specific patterns, biases, or spurious correlations that do not transfer well to a new dataset.

I think this issue is especially important in fake news detection. Different datasets often differ in text length, topic distribution, label design, source type, and annotation criteria. As a result, a model that performs well on one benchmark may not generalise well to another. For this reason, cross-dataset evaluation should not be treated as only an optional extra experiment, but as an important later stage of the project.

Recent fake news detection studies also support this direction. Some more recent work evaluates transformer-based or LLM-assisted methods on multiple fake news datasets, which suggests that modern fake news detection should not be discussed only on a single benchmark. At the same time, I think it is important to distinguish two ideas clearly: **using multiple datasets** is not the same as **training on one dataset and testing on another**. The first is closer to multi-dataset evaluation, while the second is closer to the strict cross-dataset transfer setup that I want to study later in this dissertation.

Overall, the literature supports the current structure of the project. First, I establish a stable in-domain baseline line on LIAR. Second, I use class-sensitive metrics and error analysis to understand why the models behave in the way they do. Third, I can then move to the cross-dataset stage, where the main question becomes not only which model scores slightly higher on one benchmark, but which model generalises better when the data distribution changes.
