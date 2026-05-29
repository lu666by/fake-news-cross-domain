# Plan (Next 2 Weeks)

_Last updated: 2026-05-29_

## Current context

The project now has a working dissertation story to confirm with the supervisor:

1. LIAR in-domain baselines are established.
2. Strict LIAR-to-FakeNewsNet direct transfer fails badly.
3. Intermediate target-domain fine-tuning recovers performance in the current seed-42 pass.
4. TELLER-like reasoning atoms are useful only as exploratory supporting analysis.
5. The dissertation draft has been updated and layout-checked.

## Priority 1: Supervisor meeting and framing confirmation

Goal:

- Confirm that the current framing is acceptable: reproducible baselines, strict transfer failure, and target-domain fine-tuning recovery.

Discussion points:

- Is the current seed-42 intermediate fine-tuning result enough as the main "recovery" contribution, or does it need more seeds before final submission?
- Should 10% and 20% target fine-tuning be repeated across more seeds?
- Should the TELLER-like pilot stay in Chapter 6, or be shortened/moved to appendix?

Files:

- `progress/supervisor_update_2026-05-29.md`
- `progress/supervisor_meeting_talking_points_2026-05-29.md`
- `thesis_writeup/dissertation_final.pdf`

## Priority 2: Strengthen experimental reliability if requested

Most likely next experiment:

- Repeat the 10% and 20% intermediate fine-tuning settings across additional seeds.

Reason:

- The current direct-transfer transformer rows are 5-seed averages, but the intermediate fine-tuning rows are currently seed 42.
- Multi-seed intermediate fine-tuning would make the recovery claim stronger.

Evidence to start from:

- `notebooks/13_intermediate_finetuning_fakenewsnet.py`
- `results/intermediate_finetuning/intermediate_finetuning_weighted_roberta_seeds_42.md`

## Priority 3: Final thesis polish

Tasks:

- Tighten Chapter 6 wording so the direct-transfer failure and adaptation recovery are easy to follow.
- Keep TELLER-like atoms clearly framed as exploratory only.
- Check tables/figures after any text changes.
- Keep `thesis_writeup/dissertation_final.pdf` in sync with the Word draft.

## Out of scope unless supervisor asks

- Full TELLER reproduction.
- New architecture design.
- Broad hyperparameter search.
- Uploading raw datasets or model checkpoints to GitHub.

## Expected next deliverables

- Supervisor-confirmed final experiment scope.
- If needed: multi-seed intermediate fine-tuning summary.
- Final dissertation text pass.
