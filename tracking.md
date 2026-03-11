# Plan + Progress Tracker

| Task | Start | Due | Steps (short) | Status | Evidence (path/link) |
|---|---:|---:|---|---|---|
| Add LLM prompts to all paper reviews | 2026-02-27 | 2026-02-27 | Add “LLM Prompt(s)” section and record the exact prompts used in each summary | Completed | papers/summaries/gururangan2020_dapt.md; papers/summaries/wang2017_liar.md; papers/summaries/wang2022_robustness_survey.md |
| Combine Plans + Progress into one table | 2026-02-27 | 2026-03-06 | Use `tracking.md` as the single entry point; keep only short pointers in plans/progress files | Completed | tracking.md; plans/plan_next_2_weeks.md; progress/progress_summary.md |
| LIAR: load + inspect dataset | 2026-03-05 | 2026-03-08 | Load train/valid/test splits; print dataset shapes, label counts, and sample statements | Completed | notebooks/01_liar_load.ipynb |
| LIAR: TF-IDF baseline + metrics | 2026-03-08 | 2026-03-12 | Train TF-IDF + Logistic Regression (optionally Linear SVM); report Accuracy, Macro-F1, and Confusion Matrix | Completed | notebooks/02_tfidf_baseline.ipynb; results/liar_baseline.md |
| Clean notes (only explainable) | 2026-03-05 | 2026-03-07 | Apply the 3-sentence test (What it means / Why it matters / Next step); remove unclear notes | Completed | notes/clean_notes.md |
