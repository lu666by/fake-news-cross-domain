# Plan (Next 2 Weeks)

_Last updated: 2026-05-10_

## Context

The LIAR in-domain baseline line is stable. At the last meeting the supervisor set three explicit priorities for the next phase, and this 2-week plan reflects those directly.

The supervisor's three priorities:

1. Investigate whether TELLER (Liu et al. 2024) can be used in this project.
2. Use the sample thesis (`QingyuWang_researchProject.pdf`) to understand the standard for an MSc literature review.
3. Begin to expand the literature review by adding the 2024 paper and more references.

A first round of work on all three priorities has been delivered this week. The plan below covers the second-round follow-up.

## Priority 1: Continue TELLER follow-up

Why:
- The supervisor specifically asked whether TELLER can be used, and if not, why not.

Already delivered:
- `papers/summaries/liu2024_teller.md` — 10-section summary based on the arXiv paper and the official GitHub repository.
- `results/teller_feasibility_note.md` — feasibility investigation. Conclusion: full reproduction is not feasible within the MSc project because the framework requires the OpenAI API for the logic-atom step and the human-designed predicate component adds further setup cost.
- `results/liar_baseline.md` Section 10 — TELLER row now uses decimal notation (`0.6773` / `0.6697`) and `Partly comparable`, instead of being treated as a direct baseline.

Next two weeks:
- Cite TELLER consistently in the lit review final pass.
- Do NOT attempt full reproduction unless API budget becomes available.
- Keep the conclusion line short and conservative when discussing it with the supervisor: TELLER is included as an advanced literature comparison, not a directly reproducible baseline.

## Priority 2: Apply the MSc literature review standard from the sample thesis

Why:
- The supervisor said the current literature review is still too short and too concept-focused.

Already delivered:
- `thesis_writeup/literature_review_requirements_note.md` — observations from `QingyuWang_researchProject.pdf` Chapter 2: the literature review is a full 19-page chapter with 48+ references, organised by research themes; literature review and methodology are strictly separated.

Next two weeks:
- Apply the 5 improvement points from the requirements note to my own draft.
- Each section of the literature review should have at least 3 papers cited with explicit contribution + limitation.

## Priority 3: Continue expanding the literature review

Why:
- The supervisor asked for a substantial expansion, including the 2024 paper and more references in general.

Already delivered (first round):
- Reference set grew from 6 papers to 12, with new entries: Liu et al. 2024 (TELLER), Liu et al. 2019 (RoBERTa), Shu et al. 2020 (FakeNewsNet), Augenstein et al. 2019 (MultiFC), Silva et al. 2021 (cross-domain fake news), Hu et al. 2024 (LLMs as bad actor / good advisor).
- New 6-section structure: datasets, traditional + transformer methods, LLM/reasoning methods, class imbalance, robustness/cross-dataset, research gap.
- Both Chinese original draft (`literature_review_draft_zh.md`) and English version (`literature_review_draft_en.md`) updated.
- `papers/reading_list.md` updated with priorities and statuses.

Next two weeks (second round):
- Add 1–2 more papers per section to bring the total closer to 15–18.
- Tighten the English version: remove any phrasing that is hard to say aloud or sounds artificially academic.
- Strengthen the research gap section with explicit inline citations.
- Optionally write 1–2 new short paper summaries in `papers/summaries/` for the highest-priority new references (RoBERTa, FakeNewsNet, TELLER is already done).

## Out of scope this 2-week window

- No broad BERT/RoBERTa tuning.
- No new baseline runs.
- No cross-dataset coding yet — only optional dataset-selection notes if time permits.
- `baseline_results_summary.md` stays as-is (only minor consistency edits already done).

## Files I expect to touch

- `thesis_writeup/literature_review_draft_en.md` (second-round expansion)
- `thesis_writeup/literature_review_draft_zh.md` (sync the Chinese draft)
- `papers/summaries/` — short new summaries for RoBERTa, FakeNewsNet (and possibly Silva 2021, Hu 2024)
- `papers/reading_list.md` — mark new summaries as Done as I add them
- `progress/progress_summary.md` — add a 2026-05-17 (or similar) entry at the next checkpoint
- `tracking.md` — update statuses of the three new task rows

## Scope control

The focus during these two weeks is thesis writing and literature review depth, not experiment breadth. Any additional experiment is only justified if it directly supports interpretation, supervisor questions, or the cross-dataset transition.
