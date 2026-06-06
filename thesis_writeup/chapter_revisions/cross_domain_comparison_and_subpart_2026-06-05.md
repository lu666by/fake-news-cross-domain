# Comparison with prior cross-domain work + within-FakeNewsNet subpart transfer (draft, 2026-06-05)

> **STATUS (2026-06-06): integrated into the thesis.** Chapter 6 §6.7 now holds the subpart-transfer table
> (Table 6.4, with both TF-IDF and weighted RoBERTa), and Chapter 7 §7.2 holds the comparison (Table 7.1).
> RoBERTa subpart results were added (`notebooks/15_...py`): in-domain PolitiFact 0.9205 / GossipCop 0.7962 Macro-F1;
> transfer PolitiFact→GossipCop 0.2860 (REAL recall 0.10, FAKE recall 0.94), GossipCop→PolitiFact 0.4722 —
> the stronger RoBERTa transfers *worse* across subparts and reproduces the FAKE-bias, strengthening the argument.
> This file is kept as the planning/record draft.

> Responds to the 2026-06-04 supervisor request: (a) compare this dissertation's transfer results
> with other cross-domain fake-news papers (which datasets, which results); (b) run small transfer
> experiments between FakeNewsNet subparts. Intended for Chapter 6 (results) / Chapter 7 (discussion);
> the per-paper datasets+results are already in Chapter 2.5.

---

## 1. New result: within-FakeNewsNet subpart transfer

FakeNewsNet minimal contains two source domains — **PolitiFact** (political, 1,056 titles) and **GossipCop** (entertainment, 22,140 titles). Until now they were only evaluated as one combined target. Following the supervisor's suggestion, each subpart is now evaluated separately and transferred between, using the same TF-IDF + class-weighted Logistic Regression baseline (title text only, binary REAL/FAKE).

**Table. Within-FakeNewsNet subpart transfer (TF-IDF + weighted LR).** In-domain rows are 5-seed 80/20 means; transfer rows are deterministic (all source → all target).

| Setting | Train → Test | Accuracy | Macro-F1 | REAL recall | FAKE recall |
|---|---|---:|---:|---:|---:|
| In-domain PolitiFact | PolitiFact → PolitiFact | 0.8377 | 0.8329 | 0.8512 | 0.8184 |
| In-domain GossipCop | GossipCop → GossipCop | 0.8311 | 0.7814 | 0.8609 | 0.7369 |
| Transfer PolitiFact → GossipCop | PolitiFact → GossipCop | 0.4244 | 0.4185 | 0.3457 | 0.6729 |
| Transfer GossipCop → PolitiFact | GossipCop → PolitiFact | 0.6193 | 0.5411 | 0.8734 | 0.2523 |

**Reading.**
- Each subpart is learnable in-domain (Macro-F1 0.78–0.83), so the titles do carry usable signal.
- Transfer **between** subparts drops sharply (Macro-F1 0.42 and 0.54), even though both are FakeNewsNet titles. This shows the domain gap is not only LIAR-vs-FakeNewsNet: it also exists **inside** FakeNewsNet, between political and entertainment news.
- The drop is **asymmetric**. PolitiFact → GossipCop collapses to 0.42 (a small political-claims model does not cover entertainment headlines). GossipCop → PolitiFact is better (0.54) because GossipCop is ~20× larger, but it still loses ~0.29 Macro-F1 versus in-domain PolitiFact and becomes REAL-biased (FAKE recall 0.25).
- This is consistent with, and reinforces, the dissertation's main argument: in-domain performance does not transfer across domains, and the cause is domain/topic shift rather than the model being weak.

Evidence: `results/fakenewsnet_subpart_transfer/fnn_subpart_transfer_tfidf.{md,csv}`; script `notebooks/14_fakenewsnet_subpart_transfer_tfidf.py`.

*Next step (optional, GPU): repeat with weighted RoBERTa to confirm the same pattern under the transformer baseline.*

---

## 2. How this dissertation's results sit against prior cross-domain work

The works reviewed in Chapter 2.5 are summarised here in one place with their datasets and headline results, next to what this dissertation measures. Direct numeric comparison is limited because most prior systems use **non-text signals (propagation graphs) or specialised architectures** and **different datasets**; the comparison is therefore about the *pattern* (does cross-domain transfer drop, and what helps), and about positioning this dissertation as a reproducible, text-only baseline.

**Table. Prior cross-domain fake-news work vs this dissertation.**

| Work | Datasets | Method | Key reported result | Uses non-text signals? |
|---|---|---|---|---|
| Silva et al. [17] | PolitiFact + GossipCop + CoAID | Dual domain-specific / cross-domain embeddings | up to +7.55% F1 over single-space; ~+25% F1 for rare domains | Yes (Twitter propagation) |
| Castelo et al. [18] | US-Election2016, PolitiFact, … | Topic-agnostic (readability/web-markup) features | ~0.86 / 0.83 accuracy; transfers better than content models | No (but web-markup features) |
| Han et al. [19] | Twitter propagation datasets | Propagation GNN + continual learning (EWC, GEM) | ~0.80–0.84 F1; reduces but does not remove cross-domain drop | Yes (propagation graph) |
| Wei et al. [20] (FADED) | New-MultiFC, FND-3 | Dual-granularity adversarial training | state-of-the-art average F1 on unseen domains | No (text), specialised arch. |
| Liguori et al. [21] (MERMAID) | 4 real-world fake-news datasets | Mixture-of-experts | up to ~30% improvement with very little target data | No, ensemble |
| Kishi et al. [22] | Kaggle, FakeNewsNet, ISOT, NELA-GT | Various; in- vs cross-dataset analysis | in-dataset macro-F1 up to ~0.99; **~17-point F1 drop cross-dataset** | No |
| **This dissertation** | **LIAR → FakeNewsNet titles; FakeNewsNet subparts** | **Reproducible text-only baselines (TF-IDF, BERT, RoBERTa, weighted); + intermediate fine-tuning** | **In-domain LIAR Macro-F1 0.64; strict LIAR→FNN transfer ~0.24 (below the always-REAL baseline); FNN subpart transfer 0.42–0.54; recovered to 0.70 (10%) / 0.75 (20%) with intermediate fine-tuning** | **No (titles/statements only)** |

**Discussion points (for Chapter 6/7).**
- The qualitative finding is shared across the literature and this work: **cross-domain transfer drops substantially**. Kishi et al. [22] report a ~17-point F1 drop; this dissertation sees a larger drop (in-domain ~0.83 → cross-subpart ~0.42; LIAR in-domain 0.64 → LIAR→FNN ~0.24), which is expected because the settings here are stricter (no target adaptation, title-only, and a larger domain gap).
- Where prior work improves transfer with **propagation graphs** [17, 19] or **specialised adversarial / mixture-of-experts architectures** [20, 21], this dissertation deliberately stays text-only and reproducible, and shows that a **simple, cheap intervention — a small amount of target-domain intermediate fine-tuning — recovers most of the lost performance** (Macro-F1 0.24 → 0.70/0.75). This is the practical contribution: it does not need social-graph data or a new architecture.
- Direct head-to-head numbers are **not** strictly comparable (different datasets, label schemes, and input signals), and the dissertation should say so explicitly rather than claim it beats or loses to these systems. The honest claim is: this work quantifies the transfer failure on a clean text-only setting and gives a low-cost recovery, complementing the heavier methods in the literature.

---

## 3. What to integrate where
- **Chapter 3 (experiment map / methodology):** add the within-FakeNewsNet subpart transfer as an experiment (E7) and a short protocol subsection.
- **Chapter 6 (results):** add the subpart-transfer table (Section 1 above).
- **Chapter 6 or 7 (discussion):** add the comparison table + discussion (Section 2 above).
- Keep the per-paper detail in Chapter 2.5 (already done); this comparison cross-references it rather than repeating full descriptions.
