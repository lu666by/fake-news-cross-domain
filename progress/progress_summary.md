# Progress Summary (living document)

> Note (for supervisor): the up-to-date task tracker is maintained in `tracking.md` as the single source of truth.  
> This file provides short narrative context only.

## Latest update: 2026-05-10 (Ireland time)

## What I did this week

This week the focus shifted from baseline tuning to thesis preparation, following the three priorities the supervisor set out at the last meeting.

### 1. Investigated TELLER (Liu et al. 2024) feasibility

I read the TELLER paper (Findings of ACL 2024) and the official GitHub repository, then wrote both a paper summary and a feasibility note.

Main findings:
- TELLER is a dual-system framework (cognition + decision) that uses an LLM to generate logic atoms from a claim, then learns logic rules to predict truthfulness. It is fundamentally different from a fine-tuned BERT/RoBERTa classifier.
- TELLER reports `0.6773` accuracy and `0.6697` Macro-F1 on the LIAR binary task, which is higher than my current weighted RoBERTa baseline (`0.6522` / `0.6396`).
- The framework requires the OpenAI API for the logic atom step. There is no local-LLM alternative documented in the repo.

Conclusion:
- Full reproduction within this MSc project is not currently feasible — the API cost on 10,240 training + 1,267 test claims is the main blocker, alongside the human-designed predicate component.
- TELLER is included as an advanced literature comparison in `liar_baseline.md` Section 10, marked `Partly comparable` (not the same type of baseline as my models).

### 2. Read the sample thesis to understand the MSc literature review standard

The supervisor shared `QingyuWang_researchProject.pdf` as a reference for what an MSc literature review should look like.

Main observations from Chapter 2:
- The literature review is a full chapter of about 19 pages (thesis pages 6–24), not a short summary.
- It uses 48+ unique references, with 1–3 inline citations per paragraph.
- It is organised by research themes (3 main sections, 10+ sub-sections), not by isolated paper summaries.
- The literature review is strictly separate from the methodology chapter; the author's own method is not described in the literature review.

I recorded these observations as 5 concrete improvement points for my own draft in `thesis_writeup/literature_review_requirements_note.md`.

### 3. Expanded the literature review draft

I rewrote the literature review to follow the structure observed in the sample thesis. The new draft is organised into six sections:

1. Fake news detection datasets and LIAR
2. Traditional and transformer-based fake news detection
3. LLM and reasoning-based fake news detection
4. Class imbalance and evaluation metrics
5. Robustness and cross-dataset generalisation
6. Research gap

The reference set grew from the original 6 papers to 12, with the new entries including Liu et al. 2024 (TELLER), Liu et al. 2019 (RoBERTa), Shu et al. 2020 (FakeNewsNet), Augenstein et al. 2019 (MultiFC), Silva et al. 2021 (cross-domain fake news), and Hu et al. 2024 (LLMs as bad actor / good advisor).

Each paper is now cited with its specific contribution and limitation, rather than being mentioned only as part of a general concept paragraph. Both a Chinese original draft (`literature_review_draft_zh.md`) and an English version (`literature_review_draft_en.md`) are in the repository.

### What is not in scope this week

- I did not run any new BERT/RoBERTa experiments and did not begin cross-dataset coding — the supervisor's three priorities took precedence.
- `baseline_results_summary.md` only received minor consistency edits earlier; the substantive update is in `liar_baseline.md` (Section 10 literature comparison row for TELLER fixed to use decimal notation and `Partly comparable`).

### Next week

- Second-round literature review expansion: add 1–2 papers per section, tighten the English, and strengthen the inline citations in the research gap section.
- Begin dataset selection notes for the cross-dataset stage (no coding yet).

---

## Previous update: 2026-04-12 (Ireland time)

## What I did this week

This week I focused on stabilising the current transformer comparison and testing the most direct follow-up ideas suggested by the current LIAR error patterns.

### 1. Extended the main transformer baselines to 5 runs
I extended the main transformer baselines so that the current comparison is no longer based on only 1 or 3 runs.

Updated 5-run results:

- **Unweighted BERT**
  - **Test Accuracy:** `0.6425 ± 0.0095`
  - **Test Macro-F1:** `0.6231 ± 0.0122`

- **Weighted BERT**
  - **Test Accuracy:** `0.6412 ± 0.0065`
  - **Test Macro-F1:** `0.6322 ± 0.0090`
  - **REAL recall:** `0.7048 ± 0.0292`
  - **FAKE recall:** `0.5591 ± 0.0447`

- **Weighted RoBERTa**
  - **Test Accuracy:** `0.6522 ± 0.0074`
  - **Test Macro-F1:** `0.6396 ± 0.0080`
  - **REAL recall:** `0.7443 ± 0.0153`
  - **FAKE recall:** `0.5335 ± 0.0199`

Main point:
- the current transformer comparison is now more reliable,
- the gains remain moderate rather than dramatic,
- but the overall pattern is stable enough to support the current stage of the project.

### 2. Completed a more concrete error analysis
I completed an error analysis comparing representative **weighted BERT** and **weighted RoBERTa** checkpoints.

The analysis now identifies concrete recurring error types rather than only reporting class-wise metrics.

Main patterns:
- `numeric_claim`
- `label_boundary_ambiguity`
- `context_dependent`

Main interpretation:
- weighted BERT is more willing to predict **FAKE**, so it achieves stronger FAKE recall,
- weighted RoBERTa appears more conservative and better calibrated overall,
- which helps explain why weighted RoBERTa is stronger overall, while weighted BERT remains valuable for FAKE-recall analysis.

### 3. Tested statement-only vs statement + context
I ran a controlled comparison using the weighted RoBERTa setup, changing only the input text:

- `statement_only`
- `statement + [CTX] + context`

Main result:
- naive context concatenation did **not** improve performance,
- it reduced:
  - test accuracy,
  - test macro-F1,
  - and FAKE recall.

Main interpretation:
- in LIAR, the `context` field often behaves more like source or venue metadata than true factual background,
- so directly concatenating it adds noise rather than useful evidence.

### 4. Tested threshold tuning for weighted RoBERTa
I scanned decision thresholds on the validation set while keeping the same trained weighted RoBERTa model.

Main result:
- threshold tuning based on validation **macro-F1** did **not** improve test performance,
- and it reduced FAKE recall on the test set.

Main interpretation:
- simply tuning the threshold for macro-F1 does not automatically solve the conservative FAKE boundary problem,
- and lower-threshold operating points may only be useful if the objective changes from macro-F1 to FAKE recall.

---

## Main findings this week

- The main transformer baselines have now been extended to **5 runs**, so the current model comparison is much more stable than before.
- **Weighted RoBERTa** is currently the strongest **overall** model.
- **Weighted BERT** remains important because it gives stronger **FAKE recall**.
- The current remaining difficulty is still concentrated in:
  - numeric claims,
  - narrow label boundaries,
  - and missing context.
- Naive context concatenation is **not** a useful next step for the current LIAR setup.
- Macro-F1-based threshold tuning is also **not** a strong direct fix for the current FAKE recall weakness.

---

## Main issue / open question

The main issue is no longer basic modelling setup.

The key question now is how to interpret the remaining performance gap and whether further model work is still worth the time, compared with literature review, thesis writing, and cross-dataset preparation.

---

## Next step for next week

The next priorities should now be:

1. expand the literature review,
2. write the current error analysis into a thesis-ready subsection,
3. finalise the current model comparison more clearly in the repo files,
4. begin planning the cross-dataset / cross-domain stage.
