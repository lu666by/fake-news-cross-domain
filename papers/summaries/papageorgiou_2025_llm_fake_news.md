# Papageorgiou et al. (2025) — *Harnessing Large Language Models and Deep Neural Networks for Fake News Detection*

## 1) Citation
- Eleftheria Papageorgiou, Iraklis Varlamis, Christos Chronis. *Harnessing Large Language Models and Deep Neural Networks for Fake News Detection.* Information 2025, 16, 297. https://doi.org/10.3390/info16040297

## 2) One-sentence takeaway
This paper compares several LLM-assisted fake news detection pipelines and finds that full-text BERT embeddings work best, while factual-segment extraction and graph-based methods are more interpretable but do not outperform the full-text baseline in their experiments.

## 3) What they propose (simple)
- **BERT-full:** Use BERT embeddings from the full news text and train a deep neural network (DNN) classifier.
- **BERT-fact:** Use an LLM to extract factual sentences from each article, convert those sentences into BERT embeddings, and train the same DNN classifier.
- **Graph-based method:** Use an LLM to extract entities and relations from each article, convert the graph labels into BERT embeddings, and classify the graph with a GCN.
- They also release **two new ISOT-derived datasets** based on LLM-extracted factual sentences and LLM-extracted document graphs.

## 4) What they tested
- Four fake news datasets:
  - **LIAR**
  - **PolitiFact fact-check data**
  - **FakeNewsNet**
  - **ISOT Fake News Dataset**
- First experiment: test the **BERT-embedding approach across multiple datasets** to examine generalization.
- Second experiment: compare **BERT-full**, **BERT-fact**, and three **GCN-based graph variants** on the ISOT dataset.
- Metrics include **accuracy, precision, recall, and F1-score**.

## 5) Evidence (beginner level, one example)
- The BERT-embedding classifier achieved different test accuracies across datasets:
  - **LIAR: 0.63**
  - **PolitiFact fact-check data: 0.28**
  - **FakeNewsNet: 0.79**
  - **ISOT: 0.99**
- On ISOT, **BERT-full** performed best:
  - **Accuracy = 0.9993**
  - **F1 = 0.9993**
- **BERT-fact** was lower but still strong:
  - **Accuracy = 0.9708**
- Graph-based approaches were clearly weaker:
  - **GCN-node = 0.8174**
  - **GCN-node-edge = 0.8082**
  - **GCN-node-edge-deeper = 0.8160**

## 6) Cost / practicality (important for MSc)
- **BERT-full** is the strongest baseline in this paper, but it depends on full-text input and can be more computationally expensive.
- **BERT-fact** adds an extra LLM extraction step, so it is more complex than a plain BERT baseline.
- **Graph-based methods** require LLM-based graph extraction plus GCN training, which makes the pipeline much heavier and harder to reproduce.
- For an MSc project, the simplest practical takeaway is: **start from a strong BERT baseline before trying more complex LLM pipelines**.

## 7) How I will use it in my project (direct mapping)
- My project focuses on **fake news detection with LIAR**, so this paper is useful because it includes **LIAR** in its experiments.
- It supports using **BERT as a modern baseline** before testing more advanced ideas.
- It also supports an important thesis argument: **more complex feature extraction does not automatically outperform a strong text-only transformer baseline**.
- The paper is also useful for discussing **cross-dataset generalization problems**, since the same BERT-based approach behaves very differently across datasets.

## 8) Risks / notes (simple)
- A major limitation is **poor cross-dataset generalization**.
- The best-performing method in the paper relies on **full text**, which may reduce interpretability and increase compute cost.
- The paper suggests that factual extraction and graph extraction may underperform because the LLMs used were **generic rather than task-specific fine-tuned models**.
- The authors also mention **computational cost** and **ethical concerns** as open challenges.

## 9) LLM Prompt(s) Used
You are helping me read an academic paper for my MSc thesis.

Task:
1) First, write an overall summary of the paper in 150–250 words (plain English).
2) Then, produce structured notes with sections 1–8 exactly as below.

Sections (1–8):
1) Citation (as given)
2) One-sentence takeaway
3) What they propose (simple)
4) What they tested (datasets/tasks)
5) Key evidence (beginner-level, 2–4 bullets)
6) Cost / practicality for an MSc
7) How I can use this in my project (cross-dataset fake news detection)
8) Risks / notes

Constraints:
- Use ONLY the text I paste below. Do not add outside facts.
- If something is missing, write “Not mentioned”.
- Use short bullet points for sections 3–8.
- If you make an inference, clearly label it as “Inference”.
- Keep wording simple and clear.

