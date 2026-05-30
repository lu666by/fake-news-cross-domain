# Chapter 6 Internal Rerun Update

Date: 2026-05-30

Status: internal draft. Do not make this the main supervisor reading package yet. The supervisor-facing material should lead with Chapter 2, Chapter 3, and the short updated results summary.

## Internal Claims That Are Now Safer

- The titles-only direct transfer baseline is consistently weak across five seeds. The 5-seed mean Macro-F1 is 0.2364, and the model remains strongly FAKE-biased on FakeNewsNet titles.
- The 10% intermediate fine-tuning setting is stable across five seeds. Mean Macro-F1 is 0.7035, compared with 0.2364 for the paired direct-transfer baseline.
- The 20% intermediate fine-tuning setting is also stable across five seeds and is currently the strongest absolute target-fraction result, with mean Macro-F1 0.7463 and mean Accuracy 0.8243.
- The 10% subset must be described as stratified target-title training, not as a 1:1 balanced subset.
- The completed 20% rerun now supports a five-seed claim. The remaining judgement is whether the thesis should emphasize 10% for data efficiency or 20% for best absolute performance.
- The 1000-row TELLER-like atom experiment should remain a current-setup pilot. It can support motivation and future work, but it should not be framed as a strong empirical conclusion from one random sample.

## Suggested Chapter 6 Wording

The five-seed rerun confirms that the poor direct-transfer result is not an artefact of seed 42. Across seeds 42, 52, 62, 72, and 82, the LIAR-trained weighted RoBERTa model achieves only 0.2364 mean Macro-F1 on the held-out FakeNewsNet title test set and predicts FAKE for most target examples. This establishes a stable source-only transfer failure rather than an isolated bad run.

By contrast, 10% intermediate fine-tuning gives a stable improvement over the direct baseline. The model is first fine-tuned on LIAR and then further fine-tuned on a stratified 10% FakeNewsNet target-training title subset. Across five seeds, this setting reaches 0.7035 mean Macro-F1 and 0.8083 mean accuracy on the same held-out target test split. The improvement is therefore large and repeatable, although FAKE recall remains lower than REAL recall.

The 20% target-fraction rerun confirms that the larger target subset is also stable across the same five seeds. It reaches 0.7463 mean Macro-F1 and 0.8243 mean accuracy, making it the best absolute five-seed target-fraction result so far. The thesis framing should therefore distinguish between the 10% setting as the efficient adaptation result and the 20% setting as the strongest absolute result.

## Updated Integrated Table

# Integrated Experiment Results Table

- Date: 2026-05-30
- Purpose: one-table view of in-domain baseline, direct transfer, intermediate fine-tuning, and TELLER-like pilot.
- Important: the held-out titles-only direct-transfer row plus the 10% and 20% intermediate fine-tuning rows now use the 2026-05-30 5-seed reruns.
- Important: the 5% intermediate fine-tuning row is still seed-42 only and should be treated as internal draft evidence until rerun.
- Important: target fractions are stratified fractions of the FakeNewsNet target-train title split, not 1:1 class-balanced subsets.
- TELLER-like rows are exploratory DeepSeek V4 Flash atom-pilot results; describe them only as current-setup evidence.

| block | setting | decision_model | training_data | test_data | runs | target_fraction | target_train_n | accuracy | macro_f1 | real_recall | fake_recall | note |
|:-------------------------|:--------------------------------------------------|:------------------------------------------------|:--------------------------------------------------------|:--------------------------------------|:---------------|:------------------|-----------------:|-----------:|-----------:|--------------:|--------------:|:---------------------------------------------------------------------------------------------------------------------|
| In-domain baseline | Weighted RoBERTa on LIAR test | Weighted RoBERTa | LIAR train | LIAR test | 5 seeds | | | 0.6522 | 0.6396 | 0.7443 | 0.5335 | Existing local in-domain transformer baseline. |
| Direct transfer baseline | LIAR -> FakeNewsNet combined titles | Weighted RoBERTa | LIAR train | FakeNewsNet combined titles | 5 seeds | 0% | 0 | 0.2718 | 0.2358 | 0.0372 | 0.9827 | Strict zero-shot direct transfer from LIAR to FNN; severe FAKE bias. |
| Direct transfer baseline | LIAR -> held-out FakeNewsNet test | Weighted RoBERTa | LIAR train | Held-out FakeNewsNet test split | 5 seeds | 0% | 0 | 0.2725 | 0.2364 | 0.0377 | 0.9842 | 2026-05-30 5-seed held-out title-test rerun; confirms severe FAKE bias rather than a seed-42 accident. |
| Intermediate fine-tuning | LIAR -> 5% FNN train -> FNN test | Weighted RoBERTa | LIAR train, then stratified 5% FNN target-train titles | Held-out FakeNewsNet test split | seed 42 | 5% | 742 | 0.7519 | 0.4292 | 1 | 0 | Seed-42 only; high accuracy is misleading because the model collapses to REAL predictions. |
| Intermediate fine-tuning | LIAR -> 10% FNN train -> FNN test | Weighted RoBERTa | LIAR train, then stratified 10% FNN target-train titles | Held-out FakeNewsNet test split | 5 seeds | 10% | 1484 | 0.8083 | 0.7035 | 0.9305 | 0.4379 | 2026-05-30 5-seed rerun; stable improvement over direct transfer, but subset is stratified rather than 1:1 balanced. |
| Intermediate fine-tuning | LIAR -> 20% FNN train -> FNN test | Weighted RoBERTa | LIAR train, then stratified 20% FNN target-train titles | Held-out FakeNewsNet test split | 5 seeds | 20% | 2969 | 0.8243 | 0.7463 | 0.9167 | 0.5444 | 2026-05-30 5-seed rerun; compare with 10% to decide whether to emphasize efficiency or best absolute performance. |
| TELLER-like pilot | LLM atoms: LIAR atoms -> FakeNewsNet atoms | Logistic Regression on DeepSeek-generated atoms | LIAR train+valid atom features | Balanced FakeNewsNet atom test sample | 1000-row pilot | | | 0.53 | 0.4405 | 0.13 | 0.93 | Current DeepSeek V4 Flash reasoning-atom setup shows limited performance in this pilot. |
| TELLER-like pilot | LLM atoms: FakeNewsNet atoms -> FakeNewsNet atoms | Logistic Regression on DeepSeek-generated atoms | Balanced FakeNewsNet train atom sample | Balanced FakeNewsNet atom test sample | 1000-row pilot | | 200 | 0.6 | 0.6 | 0.59 | 0.61 | Target-domain atom upper-bound pilot for the current setup; not a main contribution. |

## Main Reading

- Direct LIAR -> FakeNewsNet title transfer is consistently weak across seeds: mean Macro-F1 is 0.2364 and the model still predicts FAKE for most target examples.
- The 10% intermediate fine-tuning rerun is a stable data-efficient improvement: mean Macro-F1 is 0.7035 across five seeds, with a mean uplift of 0.4671 over source-only direct transfer.
- The 20% intermediate fine-tuning rerun is currently the strongest absolute five-seed target-fraction result: mean Macro-F1 is 0.7463, Accuracy is 0.8243, REAL recall is 0.9167, and FAKE recall is 0.5444.
- The supervisor-facing framing question is whether to emphasize the efficiency of 10% or the best absolute performance of 20%.
- The TELLER-like 1000-row atom experiment remains a pilot. It can support discussion about the current DeepSeek V4 Flash reasoning-atom setup, whose performance is limited in this pilot.
