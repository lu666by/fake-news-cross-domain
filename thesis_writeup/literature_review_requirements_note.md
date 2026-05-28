# Literature Review Requirements Note

**Based on:** QingyuWang_researchProject.pdf (MSc thesis, University of Galway, supervisor: Dr. Josephine Griffith, August 2025)
**Purpose:** Understand the standard for a MSc literature review before improving my own draft.

---

## 1. What I observed in the sample thesis

### 1.1 Length and scope

The sample thesis has **152 pages** in total. Chapter 2 (Literature Review) spans **pages 6–24 in thesis numbering** — approximately **19 pages of content**. This is not a short summary. It is a full, standalone chapter.

My current draft is only a few paragraphs. This is significantly shorter than what is expected.

### 1.2 Chapter structure

Chapter 2 has **3 main sections** and **10+ sub-sections**:

```
Chapter 2: Literature Review
  2.1 Overview of Collaborative Filtering
      2.1.1 Traditional Recommendation Methods
      2.1.2 The Main Paradigms of Collaborative Filtering
      2.1.3 The Core Ideas of Collaborative Filtering
      2.1.4 Deep Learning for Collaborative Filtering
      2.1.5 Explainability in Recommender Systems
  2.2 Overview of Knowledge Graphs
      2.2.1 Structure of Knowledge Graphs
      2.2.2 Knowledge Graphs: Construction Process
      2.2.3 Explainability of Knowledge Graphs
  2.3 Integration Methods of RecSys and Knowledge Graphs
      2.3.1 Feature-Based Recommendation Methods
      2.3.2 Path-Based Recommendation Models
      2.3.3 Collaborative Knowledge Graphs Recommendation Models
```

The structure follows research themes, not individual papers. Each main section covers a line of research, and sub-sections break it down by approach or concept.

### 1.3 Citation density

The citations in Chapter 2 run from [12] through [60]+ — roughly **48+ unique references** within the literature review chapter alone. Every paragraph has at least 1–3 inline citations. References appear like: `Abdollahi and Nasraoui [36] proposed an Explainable Matrix Factorization (EMF) model.`

The pattern is consistent:
- Name the paper and authors
- Describe what it proposes / what method it uses
- State what the paper shows or achieves (metrics, comparisons)
- Sometimes note limitations or what remains unresolved

### 1.4 Writing style

The sample thesis writes like this:

> "Zhang et al. [37] introduced a model-based collaborative filtering method called the Explicit Factor Model (EFM). This model not only utilises rating data but also incorporates item features and sentiment analysis of user reviews to produce explainable recommendations. [...] demonstrating strong performance across multiple tasks."

> "Abdollahi and Nasraoui [36] proposed an Explainable Matrix Factorization (EMF) model. This model generates interpretable Top-N item rankings and introduces new explanation quality metrics. The EMF model achieved competitive rating prediction accuracy (RMSE ≈ 0.89, nDCG@10 stable) and significantly outperformed baselines in explainability."

Key features:
- Specific paper → specific method name → specific contribution → specific result
- NOT just "some researchers have studied explainability"
- NOT just defining a concept without a citation
- Each paragraph typically covers 1–3 related papers and their contributions

### 1.5 Literature review vs methodology — they are separate chapters

Chapter 2 (Literature Review) discusses **previous work only**. It does not describe the thesis's own method, its own dataset, or its own experiments.

Chapter 3 (Methodology) is a completely separate chapter starting at page 25. It is where the author's own system design is explained.

This means: my literature review should not include sentences like "In this project, I use..." or "My approach is...". Those belong in the methodology chapter.

### 1.6 Research gap — where it appears

The research gap in the sample thesis is mainly introduced in **Chapter 1 (Research Questions, p.2)**, not at the end of Chapter 2. However, the end of Chapter 2 (e.g., Section 2.2.3 and 2.3.3) discusses the limitations of existing approaches, which implicitly motivates the research gap.

The pattern is: *existing methods have limitations X → this creates the gap → my work addresses it.*

---

## 2. What I need to improve in my own draft

Based on the sample thesis, here are **5 concrete things** to fix:

### Fix 1 — Add many more references (currently: ~6 papers, target: 15–20+)

Each section of my literature review needs at least 3–5 papers cited with specific contributions and results. My current draft mentions concepts without enough citations or paper-specific detail.

Priority papers to add:
- Liu et al. 2019 (RoBERTa) — §2 Transformer-based methods
- Shu et al. 2020 (FakeNewsNet) — §1 Datasets
- Liu et al. 2024 (TELLER) — §3 LLM/reasoning-based methods
- Hu et al. 2024 (Bad Actor, Good Advisor) — §3 LLM/reasoning-based methods
- Silva et al. 2021 (Embracing Domain Differences) — §5 Cross-domain

### Fix 2 — Each paragraph must name the paper and its contribution specifically

Do NOT write: *"Many studies have explored transformer models for fake news detection."*

DO write: *"Liu et al. [N] introduced RoBERTa, which improved upon BERT's pre-training by training on larger datasets and removing the NSP objective. RoBERTa achieved state-of-the-art results on GLUE and SQuAD benchmarks, and has since become a strong baseline for fake news detection tasks."*

### Fix 3 — Organise by research lines, not isolated paper summaries

The structure should group papers by approach. For example, Section 2 should cover:
- Traditional ML methods first (TF-IDF, SVM, logistic regression)
- Then BERT-based methods
- Then RoBERTa and similar optimised transformers

Each group should be described as a line of research, with multiple papers cited together.

### Fix 4 — Keep my own method out of the literature review

Remove or move any sentence that describes what I did, what I chose, or why I chose it. The literature review covers the field; the methodology chapter covers my project.

### Fix 5 — Add a research gap section at the end

Section 6 of my literature review should explicitly state:
- What the field has achieved so far
- What remains unresolved (cross-dataset generalisation, class imbalance under domain shift, cost of LLM-based systems)
- Why my research direction is necessary

This section should connect naturally from the previous sections and make a clear argument for why my dissertation topic matters.

---

## 3. Target structure for my literature review

```
Chapter 2: Literature Review

  2.1 Fake News Detection Datasets and LIAR
      — Wang (2017), Shu et al. (2020), Augenstein et al. (2019)
      — What each dataset covers, what limits it has

  2.2 Traditional and Transformer-Based Fake News Detection
      — Rashkin et al. (2017), Pérez-Rosas et al. (2018) [traditional]
      — Devlin et al. (2019) BERT, Liu et al. (2019) RoBERTa
      — Papageorgiou et al. (2025)

  2.3 LLM and Reasoning-Based Fake News Detection
      — Liu et al. (2024) TELLER
      — Hu et al. (2024) Bad Actor Good Advisor
      — Pan et al. (2023) program-guided reasoning

  2.4 Class Imbalance and Evaluation Metrics
      — Henning et al. (2023) class imbalance survey
      — Johnson & Khoshgoftaar (2019)

  2.5 Robustness and Cross-Dataset Generalisation
      — Wang et al. (2022) robustness survey
      — Gururangan et al. (2020) DAPT
      — Silva et al. (2021) Embracing Domain Differences
      — Papageorgiou et al. (2025) multi-dataset evaluation

  2.6 Research Gap
      — What has been achieved
      — What remains unresolved
      — Why this dissertation is needed
```

Each section should be at least half a page, with inline citations. Total target: 8–12 pages for the full chapter.
