# Supervisor Meeting Outline - 2026-05-30 14:30

Opening sentence:
I have checked the rerun evidence and updated the supervisor-facing material. The key point is no longer "I ran some experiments", but "I verified which results are stable, which ones are still uncertain, and where I need your judgement for the next step."

## 1. Completed Reruns

- Titles-only direct transfer baseline: reran Weighted RoBERTa from LIAR to held-out FakeNewsNet titles with 5 seeds: 42, 52, 62, 72, 82.
- Intermediate fine-tuning 10%: reran LIAR -> stratified 10% FakeNewsNet target-train titles -> held-out FakeNewsNet title test with the same 5 seeds.
- Intermediate fine-tuning 20%: reran LIAR -> stratified 20% FakeNewsNet target-train titles -> held-out FakeNewsNet title test with the same 5 seeds.
- Dataset-shift analysis: produced short explanatory evidence on LIAR vs FakeNewsNet title length, vocabulary overlap, and dataset-distinctive terms.
- LLM/DeepSeek atom pilot: kept as a 1000-row exploratory pilot only. The safe wording is that the current DeepSeek V4 Flash reasoning-atom setup shows limited performance in this pilot.

## 2. Main Findings

- Direct titles-only transfer is consistently weak, not just unlucky seed 42: 5-seed mean Macro-F1 is 0.2364, with very low REAL recall and high FAKE recall.
- 10% intermediate fine-tuning is a stable data-efficient improvement: 5-seed mean Macro-F1 is 0.7035, compared with 0.2364 for source-only direct transfer.
- 20% intermediate fine-tuning is now the strongest absolute 5-seed target-fraction result: mean Macro-F1 is 0.7463, Accuracy is 0.8243, REAL recall is 0.9167, and FAKE recall is 0.5444.
- The 10% subset is stratified target-title training, not 1:1 balanced sampling. I have corrected the wording in the results table and Chapter 3 terminology.
- The dataset-shift analysis supports the explanation: LIAR statements and FakeNewsNet titles differ in length, vocabulary, topic, and class distribution.

## 3. Still Uncertain

- The 5% intermediate fine-tuning row is also seed 42 only and collapses to almost all REAL predictions, so it is not a stable claim.
- Note on "titles vs full text": FakeNewsNet Minimal provides titles only, with no article body text available locally, so there is no full-body version to compare against. The two numbers seen previously (held-out title test 0.2364 vs combined titles 0.2358) are both title-based and effectively the same. The transfer experiment is therefore a LIAR-statement to FakeNewsNet-title setting, not full-article detection.
- The main framing choice is now between emphasizing 10% as the efficient adaptation result or 20% as the best absolute result.
- The 1000-row LLM/DeepSeek atom pilot is one sample only. It can support motivation, but it should not be used as a main empirical conclusion.
- Chapter 6 can be internally updated, but Chapter 2/3 plus the compact result summary are better for supervisor review first.

## 4. Decisions Needed From Supervisor

- Should the thesis main claim focus on "strict direct transfer fails, small target-domain intermediate fine-tuning helps"?
- Should I frame the main intermediate fine-tuning claim around 10% efficiency, 20% best absolute performance, or show both as complementary?
- Should the 1000-row LLM/DeepSeek atom pilot remain in Chapter 6 as a short supporting analysis, or move mostly to future work / appendix?
- Is Chapter 2/3 now clear enough as the supervisor-facing reading package, or should I reduce the literature review further before sending the full dissertation draft?

Files ready for the meeting:

- Chapter 2/3 supervisor version: `thesis_writeup/supervisor_materials_20260530/supervisor_ch2_ch3_results_2026-05-30.pdf`
- Updated integrated result table: `results/integrated_experiment_summary/integrated_main_results_table.md`
- Internal Chapter 6 rerun note: `thesis_writeup/supervisor_materials_20260530/chapter6_internal_rerun_update_2026-05-30.md`
