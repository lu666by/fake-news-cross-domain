# Wang (2017) — “Liar, Liar Pants on Fire”: A New Benchmark Dataset for Fake News Detection (LIAR)

## 1) Citation
- William Yang Wang. “Liar, Liar Pants on Fire: A New Benchmark Dataset for Fake News Detection.” ACL 2017. doi:10.18653/v1/P17-2067

## 2) One-sentence takeaway
LIAR is a claim-level fake news benchmark with short political statements and 6 fine-grained truthfulness labels; it is useful for in-domain evaluation, but its label granularity + claim-style text can make cross-dataset transfer harder.

## 3) What problem does this paper solve?
- Fake news detection lacked a reasonably large, manually labeled dataset.
- Many earlier resources were too small for typical ML evaluation, especially for short political statements.

## 4) Dataset details (core facts)
- Data source: PolitiFact (via API), fact-checked short statements.
- Unit of text: short statement/claim (not full news article).
- Size: 12,836 statements.
- Splits:
  - Train: 10,269
  - Validation: 1,284
  - Test: 1,283
- Average statement length: ~17.9 tokens (very short).
- Labels (6 classes): pants-fire, false, barely-true, half-true, mostly-true, true.
- Metadata included (examples): subject, context/venue, speaker, state, party, and speaker history/credit history.
- Time span: mainly 2007–2016.
- Quality check: authors report agreement (Cohen’s kappa) of 0.82 on a sampled subset.

## 5) Baselines / experiments (high level)
- Task framing: 6-way multi-class classification.
- They compare standard text models (LR, SVM, BiLSTM, CNN) and a hybrid CNN that can combine text + metadata.
- Metric: accuracy (they claim it is similar to F1 on this relatively balanced dataset).

## 6) Main findings (simple numbers to remember)
- Majority baseline ~0.208 test accuracy.
- Text-only CNN ~0.270 test accuracy (best among text-only).
- Hybrid CNN with “text + all metadata” ~0.274 test accuracy (small improvement over text-only CNN).
- BiLSTM underperformed (they mention overfitting).

## 7) Limitations / assumptions (important for thesis)
- Claim-level and very short text: different from article-style datasets (e.g., FakeNewsNet).
- Fine-grained labels can be ambiguous and hard to align with other datasets (binary vs multi-class, different label definitions).
- Fact-check labels depend on journalistic judgment and evidence; not a typical “simple labeling” task.

## 8) Relevance to my MSc (beginner-friendly)
- This is the “must-cite” paper if I use LIAR.
- It helps me explain why cross-dataset transfer may fail: LIAR is short claims + 6-way labels, while other datasets may be long articles + different labeling rules.
- It gives me realistic baseline expectations (linear models and CNN are competitive; RNN may overfit here).
- For cross-dataset experiments, I will likely map 6 labels → 2 labels (true-ish vs false-ish) to make datasets comparable.

## 9) Questions / notes
- Q1: For my project, should I keep LIAR as 6-way, or convert to binary to match FakeNewsNet?
- Q2: If I use metadata, do I risk “leakage” (e.g., speaker history features that indirectly encode the label)?
## 10) LLM Prompt(s) Used
You are helping me read an academic paper for my MSc thesis.

Task:
1) First, write an overall summary of the paper in 150–250 words (plain English).
2) Then, produce structured notes with sections 1–8 exactly as below.

Sections (1–8):
1) Citation (as given)
2) One-sentence takeaway
3) What they propose (simple)
4) What they tested (datasets/tasks)
5) Key evidence (beginner-level, 2–4 bullets)
6) Cost / practicality for an MSc
7) How I can use this in my project (cross-dataset fake news detection)
8) Risks / notes

Constraints:
- Use ONLY the text I paste below. Do not add outside facts.
- If something is missing, write “Not mentioned”.
- Use short bullet points for sections 3–8.
- If you make an inference, clearly label it as “Inference”.
- Keep wording simple and clear.


