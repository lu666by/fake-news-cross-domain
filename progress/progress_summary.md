# Progress Summary (living document)

> Note (for supervisor): The up-to-date plan + progress tracker is maintained in `tracking.md` (single source of truth).  
> This file provides short narrative context only.

## Latest update: 2026-03-12 (Ireland time)

### What I have achieved

Over the past two weeks I focused on moving from planning to implementation.

1. **Repository organisation and tracking**
   - Maintained a single tracker table in `tracking.md` to record task status and evidence links.
   - `plans/` and `progress/` files now contain short contextual notes and point to `tracking.md` for the current status.

2. **Initial LIAR dataset implementation**
   - Implemented `notebooks/01_liar_load.ipynb` to load and inspect the LIAR dataset.
   - The notebook loads the `train`, `valid`, and `test` splits and prints:
     - dataset shapes
     - label distribution
     - example statements

3. **TF-IDF baseline experiment**
   - Implemented `notebooks/02_tfidf_baseline.ipynb`.
   - Model: **TF-IDF + Logistic Regression**.
   - Evaluation metrics include:
     - Accuracy
     - Macro-F1
     - Confusion Matrix.

   Results are recorded in:

   `results/liar_baseline.md`

   The baseline achieved approximately:

   - **Accuracy ≈ 0.62**
   - **Macro-F1 ≈ 0.59**

4. **Clean research notes**
   - Updated `notes/clean_notes.md`.
   - Applied the **3-sentence test** for each item:
     - What it means
     - Why it matters
     - Next step

---

### Key takeaways so far (high level)

- Cross-dataset evaluation can be viewed as performance under **natural distribution shift (out-of-distribution / OOD)**.
- The **LIAR dataset** contains short political claims with **six truthfulness labels**, which differs substantially from news-style datasets that typically use **binary labels**.
- A simple TF-IDF baseline provides a useful reference point before moving to stronger models.

---

### Open questions / risks (only items I can clearly explain)

**Label mapping for cross-dataset experiments**

- What it means: LIAR has 6 labels, while many news datasets use binary labels (real/fake).
- Why it matters: cross-dataset experiments require a consistent label space.
- Next step: define and document a binary label mapping when preparing cross-dataset evaluation.

**Model robustness across datasets**

- What it means: models trained on one dataset may not generalise well to another dataset.
- Why it matters: this is central to the dissertation research question.
- Next step: after establishing in-domain baselines, test cross-dataset transfer.

---

### Next actions (implementation focus)

The next implementation steps are:

1. Implement a **stronger baseline model** (e.g., BERT-based classifier).
2. Prepare the pipeline for **cross-dataset evaluation**.
3. Compare **in-domain vs cross-dataset performance drop**.

Dates and detailed task status are tracked in:

`tracking.md`
