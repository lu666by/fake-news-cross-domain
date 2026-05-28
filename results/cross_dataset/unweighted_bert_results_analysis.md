# Unweighted BERT vs Weighted BERT: Cross-Dataset Transfer Results

## Experiment Completed ✅

5 seeds × 3 epochs, all results saved to `results/cross_dataset/`.

---

## Side-by-Side Comparison: FakeNewsNet Combined Titles

| Metric | Unweighted BERT | Weighted BERT | Δ |
|--------|-----------------|---------------|---|
| **Accuracy** | 0.3018 ± 0.0191 | 0.2935 ± 0.0234 | +0.0083 |
| **Macro-F1** | 0.2806 ± 0.0275 | 0.2682 ± 0.0342 | +0.0124 |
| **REAL recall** | 0.0890 ± 0.0349 | 0.0747 ± 0.0414 | +0.0143 |
| **FAKE recall** | 0.9467 ± 0.0294 | 0.9564 ± 0.0320 | -0.0097 |

## LIAR In-Domain Comparison

| Metric | Unweighted BERT | Weighted BERT |
|--------|-----------------|---------------|
| Accuracy | 0.6425 ± 0.0095 | 0.6412 ± 0.0065 |
| Macro-F1 | 0.6231 ± 0.0122 | 0.6322 ± 0.0090 |
| REAL recall | 0.7706 ± 0.0110 | 0.7048 ± 0.0292 |
| FAKE recall | 0.4770 ± 0.0281 | 0.5591 ± 0.0447 |

## PolitiFact Titles Comparison

| Metric | Unweighted BERT | Weighted BERT |
|--------|-----------------|---------------|
| Accuracy | 0.5114 ± 0.0560 | 0.4835 ± 0.0453 |
| Macro-F1 | 0.4805 ± 0.0803 | 0.4371 ± 0.0710 |
| REAL recall | 0.2436 ± 0.1135 | 0.1782 ± 0.0995 |
| FAKE recall | 0.8981 ± 0.0333 | 0.9245 ± 0.0392 |

---

## Key Finding: Scenario B Confirmed

> [!IMPORTANT]
> **Removing weighted loss does NOT fix the transfer problem.**
> Unweighted BERT still massively over-predicts FAKE on FakeNewsNet titles (FAKE recall ~0.95, REAL recall ~0.09).
> The improvement is marginal (+0.014 REAL recall on combined titles).

### Interpretation

The main cause of poor LIAR → FakeNewsNet transfer is **dataset distribution shift**, not weighted loss:

1. **LIAR statements** are political fact-checking claims (short, formal, factual style)
2. **FakeNewsNet titles** are news headlines (clickbait, sensational, informal style)
3. The BERT model learns LIAR-specific patterns that look "FAKE-like" when applied to news titles
4. Even without class weight bias, the model still classifies ~95% of FakeNewsNet samples as FAKE

### What this means for the thesis

- Weighted loss contributes a small amount to FAKE over-prediction, but it is **not the primary cause**
- The **fundamental problem is domain/distribution shift** between LIAR and FakeNewsNet
- This **supports the core research question**: cross-dataset generalisation is a real and substantial challenge
- Next experiments should explore **domain adaptation** or **multi-dataset training** rather than just tuning loss weights

---

## 导师 Meeting 口头回答要点

如果导师问 "What did the unweighted BERT experiment show?"：

> "I ran unweighted BERT trained on LIAR and tested on FakeNewsNet titles.
> Even without class weights, the model still over-predicts FAKE — REAL recall is only about 9%.
> So the main issue is not the weighted loss, it's the distribution shift between LIAR statements and FakeNewsNet titles.
> This confirms that cross-dataset generalisation is a real challenge, which is exactly my research question."

如果导师问 "So what's next?"：

> "Since weighted loss is not the main issue, the next step could be domain adaptation —
> for example, continued pre-training on target domain text, or training on combined data from both datasets."

---

## Output Files Generated

- [cross_dataset_unweighted_bert_liar_to_fakenewsnet.md](file:///c:/Users/lby/Downloads/v2/results/cross_dataset/cross_dataset_unweighted_bert_liar_to_fakenewsnet.md)
- `results/cross_dataset/cross_dataset_unweighted_bert_liar_to_fakenewsnet.csv`
- `results/cross_dataset/cross_dataset_unweighted_bert_liar_to_fakenewsnet_summary.csv`
- `results/cross_dataset/cross_dataset_unweighted_bert_liar_to_fakenewsnet_full.csv`
- `results/cross_dataset/cross_dataset_unweighted_bert_training_history.csv`
- `results/cross_dataset/figures/unweighted_bert_cross_dataset_metrics.png`
- `results/cross_dataset/figures/unweighted_bert_fakenewsnet_combined_confusion_matrix.png`
