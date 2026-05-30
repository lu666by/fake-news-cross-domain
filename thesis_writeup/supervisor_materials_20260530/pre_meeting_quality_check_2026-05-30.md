# Pre-Meeting Quality Check - 2026-05-30

Scope checked:

- Updated integrated result table.
- 5-seed titles-only direct transfer summary.
- 5-seed 10% intermediate fine-tuning summary.
- 5-seed 20% intermediate fine-tuning summary.
- Supervisor-facing Chapter 2/3 document.
- Internal Chapter 6 rerun note.
- Dataset-shift analysis figures and report.
- LLM/DeepSeek reasoning-atoms pilot wording.
- Rerun runbook file references.

## Numeric Consistency

Status: passed.

- Titles-only held-out direct transfer mean/std were recomputed from the five per-seed rows.
- 10% intermediate fine-tuning mean/std were recomputed from the five per-seed rows.
- 20% intermediate fine-tuning mean/std were recomputed from the five per-seed rows.
- The integrated result table values match the rounded source means:
  - Direct transfer held-out: Accuracy 0.2725, Macro-F1 0.2364, REAL recall 0.0377, FAKE recall 0.9842.
  - 10% intermediate FT: Accuracy 0.8083, Macro-F1 0.7035, REAL recall 0.9305, FAKE recall 0.4379.
  - 20% intermediate FT: Accuracy 0.8243, Macro-F1 0.7463, REAL recall 0.9167, FAKE recall 0.5444.
- 20% full CSV has 10 rows: 5 source-only rows and 5 intermediate-FT rows; seeds are 42, 52, 62, 72, and 82; target_fraction is 0.2; test_n is 4640; target_train_n is 2969 for every 20% row.
- The PowerShell training command returned a nonzero native-command status because warnings were emitted to the redirected stream, but the run saved all expected outputs. The log contains no Traceback, CUDA error, or out-of-memory error.

## File And Figure Paths

Status: passed after repair.

- Checked 43 referenced Markdown links, image links, and code-formatted local file references in the meeting materials and result reports.
- Fixed four stale runbook references that pointed to planned `0p10_0p20` output files that do not exist yet.
- Confirmed the required supervisor deliverables, updated result table, and dataset-shift figure files exist.

## Wording Safety

Status: passed after repair.

- LLM/DeepSeek/Flash wording now says the current DeepSeek V4 Flash reasoning-atom setup shows limited performance in this pilot.
- The supervisor-facing wording limits the claim to this current setup.
- The reasoning-atoms result is consistently framed as a pilot / current-setup observation, not as a main conclusion.

## Visual Check

Status: passed.

- Meeting outline PDF renders as one page.
- Updated Chapter 2/3 PDF first pages render without table overflow after the LLM wording update.
- Previous table split issue for Table 3.1 remains fixed.
