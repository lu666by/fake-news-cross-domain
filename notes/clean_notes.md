# Clean Notes (Explainable)

## What I understand clearly
- My thesis focus: cross-dataset generalisation for fake news detection.
  - Train on dataset A (source), test on dataset B (target).
  - Goal: measure domain shift and improve robustness with simple, reproducible methods.
- LIAR vs FakeNewsNet main differences:
  - Labels: LIAR has 6 truth labels; FakeNewsNet is usually binary (real/fake).
  - Text: LIAR is short claims; FakeNewsNet is news-style text (often longer).
  - Because of this, a model trained on one dataset may drop a lot on the other (domain shift).
- For an MSc, I should prioritise:
  - simple baselines first (TF-IDF + LR/SVM),
  - clear evaluation (in-domain vs cross-domain),
  - transparent documentation (prompts, tracker, clean notes).

## Decisions I need to make (and I can explain)
- Decision 1: LIAR label setting for the first baseline
  - Option A: start with 6-class in-domain baseline (simpler, matches LIAR labels).
  - Option B: convert LIAR to binary early (useful for later cross-dataset alignment).
  - My plan: do 6-class in-domain baseline first, then add a binary version for cross-dataset work.
- Decision 2: Text field choice for each dataset (to reduce mismatch)
  - LIAR: use `statement`.
  - FakeNewsNet: likely use `title` or a consistent short text field (to reduce length/style mismatch).

## Questions I can explain (with reason)

### Q1: Why do I need label mapping?
- What it means:
  - Mapping is only needed when I compare across datasets with different label spaces.
  - LIAR has 6 labels; FakeNewsNet is usually binary.
- Why it matters:
  - Without a shared label space, cross-dataset evaluation is not meaningful.
- Next step:
  - Run LIAR in-domain baseline first.
  - Then define a clear binary mapping and document it.

### Q2: What is my binary mapping idea (for cross-dataset)?
- What it means:
  - Convert LIAR 6 labels into 2 labels so it aligns with binary datasets.
- Why it matters:
  - It enables train-on-A test-on-B experiments.
- Next step:
  - Start with a simple rule:
    - true / mostly-true / half-true → REAL
    - barely-true / false / pants-fire → FAKE
  - Do a small robustness check: exclude `half-true` and see if results change a lot.

### Q3: What baselines will I run first?
- What it means:
  - Start with traditional ML baselines before complex models.
- Why it matters:
  - Baselines are fast, reproducible, and give a clear reference point.
- Next step:
  - LIAR in-domain:
    - TF-IDF + Logistic Regression
    - (optional) TF-IDF + Linear SVM
  - Save results in `results/liar_baseline.md`.

### Q4: What evaluation metrics will I report?
- What it means:
  - Use Accuracy + Macro-F1 + Confusion Matrix.
- Why it matters:
  - Macro-F1 is better when classes are imbalanced.
  - Confusion matrix shows what kinds of errors increase.
- Next step:
  - Report these metrics for LIAR test split baseline.
  - Later report in-domain vs cross-domain drop (e.g., ΔMacro-F1).

### Q5: If I try TAPT/DAPT later, what is the key risk?
- What it means:
  - Data leakage if I adapt on target test text.
- Why it matters:
  - It would inflate results and is not a valid evaluation.
- Next step:
  - Only use target training text (unlabeled) or external unlabeled corpora.
  - Try TAPT first (cheaper), keep experiments small.

## Immediate next actions (after returning to Ireland)
- Create `notebooks/01_liar_load.ipynb`:
  - load train/valid/test
  - print shape + label counts + 3 sample statements
- Create `notebooks/02_tfidf_baseline.ipynb` and run TF-IDF baseline
- Fill `results/liar_baseline.md` with metrics
- Keep `tracking.md` updated with status + evidence links
