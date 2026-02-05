# Progress Summary (living document)

## Latest update: 2026-02-05 (Dublin time)

### What I have achieved (literature-focused)
- Set up and organised the repository structure for supervision:
  - `papers/` (reading list + paper summaries)
  - `plans/` (dated plans)
  - `progress/` (progress log)
- Skim-read 3 core papers and created beginner-friendly summaries (1-page style each):
  - LIAR dataset paper: `papers/summaries/wang2017_liar.md` (Done — skim)
  - Robustness/OOD survey: `papers/summaries/wang2022_robustness_survey.md` (Done — skim)
  - DAPT/TAPT paper: `papers/summaries/gururangan2020_dapt.md` (Done — skim)
- Updated `papers/reading_list.md` so the reading status and outputs are traceable.

### Key takeaways so far (high level)
- Cross-dataset evaluation can be framed as robustness under *natural distribution shift* (OOD).
- LIAR is claim-level and short-text with fine-grained labels; this is likely to mismatch with article-style datasets and different label definitions.
- Continued pretraining on unlabeled target text (DAPT/TAPT) is a simple, explainable idea for reducing domain mismatch.

### Open questions / risks
- Label alignment: LIAR (6-way) vs other datasets (often binary / different definitions) → need a defensible mapping strategy.
- Scope control: keep experiments minimal and reproducible (avoid overcomplicated pipelines).
- Compute: if adaptation is tested, TAPT may be more feasible than full DAPT.

### Next actions (dated, literature-first)
- 2026-02-06 to 2026-02-08: add and skim 2 cross-dataset generalisation papers; write 2 new summaries.
- 2026-02-09 to 2026-02-11: read FakeNewsNet dataset paper more carefully; write a complete summary.
- 2026-02-12 to 2026-02-14: draft a 1–2 page literature synthesis (definitions + gaps + minimal experiment plan).
