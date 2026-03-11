# Clean Notes (Explainable)

## What I understand clearly

- My thesis focus: **cross-dataset generalisation for fake news detection**.
  - Train on dataset A (source), test on dataset B (target).
  - Goal: measure domain shift and improve robustness using simple, reproducible methods.

- Key differences between LIAR and FakeNewsNet:
  - **Labels:** LIAR has 6 truth labels; FakeNewsNet is usually binary (real/fake).
  - **Text:** LIAR contains short political claims; FakeNewsNet contains news-style text (longer).
  - Because of these differences, models trained on one dataset may perform poorly on the other (domain shift).

- For an MSc thesis, priorities should be:
  - simple and reproducible baselines first,
  - clear evaluation setup (in-domain vs cross-domain),
  - transparent documentation (tracker, prompts, notes).

---

## Decisions I need to make (and I can explain)

### Decision 1: LIAR label setting

- Option A: run a **6-class baseline** using original LIAR labels.
- Option B: convert LIAR into **binary labels** early for cross-dataset alignment.

Current choice:
- Start with a **binary baseline** for LIAR to simplify later cross-dataset experiments.

Reason:
- Many fake news datasets use binary labels, so binary mapping simplifies comparison.

---

### Decision 2: Text field choice for each dataset

Goal: reduce dataset mismatch as much as possible.

- LIAR: use `statement`
- FakeNewsNet: likely use `title` or another short text field

Reason:
- Using shorter texts reduces style/length mismatch between datasets.

---

## Questions I can explain (with reason)

### Q1: Why do I need label mapping?

**What it means**

LIAR uses six labels, while many fake news datasets use binary labels.

**Why it matters**

Cross-dataset evaluation requires a shared label space.

**Next step**

- Run LIAR in-domain baseline first.
- Define and document a clear binary mapping for cross-dataset experiments.

---

### Q2: What binary mapping will I use?

**What it means**

Convert LIAR 6 labels into 2 labels.

**Why it matters**

This allows training on one dataset and testing on another.

**Mapping rule**


true / mostly-true / half-true → REAL
barely-true / false / pants-fire → FAKE


**Next step**

Run a robustness check:

- remove `half-true`
- compare results

---

### Q3: What baseline models should I run first?

**What it means**

Start with traditional machine learning models.

**Why it matters**

These baselines are fast, interpretable, and reproducible.

**Baseline experiments**

LIAR in-domain:

- TF-IDF + Logistic Regression
- (optional) TF-IDF + Linear SVM

Results are recorded in:


results/liar_baseline.md


---

### Q4: What evaluation metrics should I report?

**What it means**

Use standard classification metrics.

**Metrics**

- Accuracy
- Macro-F1
- Confusion Matrix

**Why it matters**

- Macro-F1 is better when classes are imbalanced.
- Confusion matrix helps identify systematic error patterns.

**Next step**

Compare:

- in-domain performance (LIAR → LIAR)
- cross-dataset performance later (A → B)

---

### Q5: If I test TAPT/DAPT later, what is the key risk?

**What it means**

There is a risk of **data leakage** if the model adapts on target test data.

**Why it matters**

This would artificially inflate results.

**Next step**

- Only use target **training text** (unlabeled) or external corpora.
- Start with **TAPT** because it is cheaper than DAPT.

---

## Immediate next actions

After completing the LIAR baseline experiment:

1. Review and document baseline results clearly.
2. Implement a stronger baseline model (e.g., BERT).
3. Prepare datasets for cross-dataset evaluation.
4. Compare performance drop between in-domain and cross-datase
