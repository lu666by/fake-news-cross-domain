# Progress Summary (living document)

> Note (for supervisor): The up-to-date plan + progress tracker is in `tracking.md` (single source of truth).
> This file provides brief narrative context only.

## Latest update: 2026-02-27 (Ireland time)

### What I have achieved
- Updated paper reviews to improve transparency:
  - Added an **“LLM Prompt(s)”** section to each paper review (with the exact prompts used).
  - Evidence examples:
    - `papers/summaries/gururangan2020_dapt.md`
    - `papers/summaries/wang2017_liar.md`
    - `papers/summaries/wang2022_robustness_survey.md`
- Improved repo organisation for supervision:
  - Maintained a single tracker table in `tracking.md` with status + evidence links.
  - Updated `plans/` and `progress/` to point to `tracking.md` as the main tracker.
- Current constraint:
  - I will travel back to Ireland on **2026-03-04** and have family medical appointments before that, so implementation tasks are scheduled to start from **2026-03-05**.

### Key takeaways so far (high level)
- Cross-dataset evaluation can be treated as performance under **natural distribution shift (OOD)**.
- LIAR is **short claim-level text** with **6-level truth labels**, which can mismatch with other datasets that are **news-style text** and often **binary labels**.
- Domain/task-adaptive pretraining (DAPT/TAPT) is a clear idea for reducing domain mismatch, but it must be tested carefully and cheaply (TAPT first).

### Open questions / risks (only items I can explain)
- **Label mapping (only needed for cross-dataset):**
  - What it means: LIAR has 6 labels; FakeNewsNet-like datasets are often binary (real/fake).
  - Why it matters: cross-dataset evaluation requires a consistent label space.
  - Next step: run LIAR **in-domain** baseline first; then define and test a binary mapping for cross-dataset experiments.
- **Scope control:**
  - Risk: spending too long on reading without implementation.
  - Next step: prioritise LIAR load + TF-IDF baseline + clear metrics first.
- **If adaptation is tested (DAPT/TAPT):**
  - Risk: data leakage if adapting on target **test** text.
  - Next step: only use target **training** text (unlabeled) or external unlabeled corpora; keep runs small.

### Next actions (implementation-first; see `tracking.md` for dates/status)
- Finalise Task 2 (single tracker): ensure `tracking.md` is the only place for status tracking; keep plans/progress as short background pointers.
- Start coding with LIAR:
  - `notebooks/01_liar_load.ipynb` (load + inspect train/valid/test; shapes; label counts; 3 samples)
  - `notebooks/02_tfidf_baseline.ipynb` (TF-IDF + LR/SVM; report Accuracy + Macro-F1 + Confusion Matrix)
  - Record results in `results/liar_baseline.md`
- Clean notes:
  - Create/update `notes/clean_notes.md` and keep only explainable notes/questions (3-sentence test).
