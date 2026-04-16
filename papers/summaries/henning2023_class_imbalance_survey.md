# Henning et al. (2023) — A Survey of Methods for Addressing Class Imbalance in Deep-Learning-Based Natural Language Processing

## 1) Citation
- Sophie Henning, William Beluch, Alexander Fraser, Annemarie Friedrich.  
  “A Survey of Methods for Addressing Class Imbalance in Deep-Learning-Based Natural Language Processing.”  
  EACL 2023, pp. 523–540.

## 2) One-sentence takeaway
Class imbalance is still a major problem in transformer-based NLP, and practical ways to address it include re-sampling, data augmentation, and changing the loss function, while more complex staged-learning or model-design methods may help but usually cost more.

## 3) Key definitions (in simple words)
- **Class imbalance**: some labels appear much more often than others, so models learn majority classes better than minority classes.
- **Minority class**: a label with relatively few training examples.
- **Majority class**: a label with many more training examples.
- **Step imbalance**: a few classes are much smaller than the others.
- **Linear imbalance / long-tailed distribution**: class frequencies gradually decrease, with many rare classes at the tail.
- **Catch-all class**: a very large “other / outside” class that makes minority labels harder to learn.
- **Macro-average / per-class evaluation**: evaluation that gives each class similar importance instead of letting majority classes dominate the score.

## 4) Evaluation implications (what this means for my MSc)
- Reporting only **accuracy** can be misleading, because accuracy mainly reflects majority-class performance.
- For imbalanced NLP tasks, it is important to report:
  - **macro-F1**
  - **per-class recall**
  - especially minority-class performance
- This is directly relevant to my LIAR binary setup, because the main weakness is still the **FAKE** class.
- The paper supports the idea that evaluating only overall accuracy is not enough when minority-class detection matters.

## 5) Why models fail (one key concept)
- Current NLP models, including transformer-based models, still perform poorly on minority classes when label distributions are skewed.
- The problem becomes worse when classes overlap in feature space, or when a large catch-all class absorbs many examples.
- The paper also notes that BERT-era models improved minority performance somewhat, but **did not solve the class imbalance problem**.

## 6) Mitigation strategies (only the categories I might use)
- **Re-sampling**
  - oversampling minority classes
  - undersampling majority classes
  - class-aware sampling
- **Data augmentation**
  - simple text augmentation
  - hidden-space augmentation
  - synthetic minority examples
- **Loss functions**
  - weighted cross-entropy
  - focal loss
  - Dice loss
  - LDAM
  - other imbalance-aware losses
- **Staged learning**
  - first learn representations
  - then rebalance or retrain the classifier
- **Model design**
  - architectures specially designed for long-tail or imbalance settings

## 7) How this connects to my project
- This is the most directly relevant survey for my **weighted BERT** line.
- It gives a clear method-level justification for using **class-weighted loss** to improve minority-class sensitivity.
- It helps explain my current result pattern:
  - weighted BERT improves **FAKE recall**
  - weighted RoBERTa gives stronger **overall performance**
- It also supports my decision to focus on:
  - **macro-F1**
  - **FAKE recall**
  rather than only raw accuracy.
- The survey is also useful for the thesis discussion section, because it explains why class-imbalance improvements are often **moderate rather than dramatic**.

## 8) Notes to reuse in proposal/introduction (short)
- Class imbalance remains a serious problem in deep-learning-based NLP, even in the transformer era.
- Accuracy alone is not a reliable metric in imbalanced tasks.
- Reporting macro-level and per-class metrics is important when minority classes matter.
- Re-sampling, augmentation, and loss-function changes are practical first choices for imbalance handling.
- Weighted loss is a reasonable and interpretable way to improve minority-class performance.

## 9) LLM Prompt(s) Used
You are helping me read an academic paper for my MSc thesis.
