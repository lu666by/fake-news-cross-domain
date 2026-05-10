# Silva et al. (2021) — *Embracing Domain Differences in Fake News: Cross-domain Fake News Detection using Multimodal Data*

## 1) Citation
- Amila Silva, Ling Luo, Shanika Karunasekera, Christopher Leckie. *Embracing Domain Differences in Fake News: Cross-domain Fake News Detection using Multimodal Data.* AAAI 2021. (arXiv:2102.06314)

## 2) One-sentence takeaway
Silva et al. show that fake news detection models trained on one domain (e.g. politics) generalise poorly to other domains (e.g. entertainment, COVID-19), and propose a framework that explicitly preserves both domain-specific and cross-domain knowledge using two embedding spaces, plus an unsupervised instance-selection method to maximise domain coverage of the labelled set.

## 3) What they propose (simple)
- **Core observation:** news from different domains differs significantly in both word usage (Figure 1a — word clouds) and propagation patterns (Figure 1b — t-tests on graph-level features), so a single-domain model transfers poorly.
- **Three modules:**
  - **Module A — Unsupervised Domain Discovery:** build a heterogeneous graph of users + words from news titles, run Louvain community detection, represent each news record's domain as a soft-membership vector over communities (no domain labels needed).
  - **Module B — Domain-agnostic Classifier:** map each news record into **two separate embedding subspaces** — one domain-specific (`f_specific`), one cross-domain (`f_shared`) — concatenate them, then train a binary classifier with a reconstruction auxiliary loss.
  - **Module C — LSH-based Instance Selection:** select unlabelled news records for manual labelling so that the labelled set maximises domain coverage, without depending on a pre-trained initial model.
- The design choice that distinguishes this work from prior cross-domain methods (e.g. Wang 2018, Castelo 2019) is that they **keep** domain-specific signal instead of trying to remove it.

## 4) What they tested
- **Datasets** combined to emulate a domain-agnostic stream:
  - **PolitiFact** (politics) — 269 fake / 230 real
  - **GossipCop** (entertainment) — 1,269 fake / 2,466 real
  - **CoAID** (COVID-19) — 135 fake / 1,568 real
- Both **text content** (titles + bodies) and **propagation networks** (Twitter retweet graphs, with a 5-hour ∆T to evaluate early detection) are used as inputs.
- Compared against several state-of-the-art fake-news detectors as baselines.

## 5) Evidence (beginner level, one example)
- The proposed framework **outperforms state-of-the-art fake-news detectors by up to 7.55% in F1-score** on the cross-domain dataset.
- The instance-selection method yields around **25% F1-score improvement for rarely-appearing domains** in the news dataset.
- The t-SNE visualisation (Figure 3) shows that the proposed multimodal domain-discovery approach gives a **clearer separation between PolitiFact, GossipCop, and CoAID** than the user-only baseline of Chen et al. 2020.
- Two-sample t-tests confirm the propagation-network differences between PolitiFact and GossipCop are statistically significant across multiple graph-level features (p as low as 3.42e-29 for propagation speed).

## 6) Cost / practicality (important for MSc)
- The full framework needs **propagation networks** (retweet graphs from Twitter), which are no longer freely re-collectable at scale due to the X/Twitter API restrictions in 2024–2026.
- The text-only side of the framework (titles + bodies) is reproducible and is the realistic part for an MSc project.
- The two-subspace classification idea (one domain-specific, one shared) is **lightweight conceptually** and could be approximated with a small adapter on top of fine-tuned BERT/RoBERTa.
- For my project, the value of this paper is mainly **conceptual** (motivating the cross-dataset stage and explaining *why* a LIAR-only model is unlikely to transfer), not as a system to fully reproduce.

## 7) How I will use it in my project (direct mapping)
- This is the **central reference** for the cross-dataset / cross-domain stage of my project.
- It directly motivates why training on LIAR alone is insufficient: my project's stated direction (cross-dataset generalisation) is exactly the gap Silva et al. identify.
- I will cite it in two places in the literature review:
  - **"Robustness and cross-dataset generalisation"** section — as the main empirical evidence that single-domain models drop significantly when tested cross-domain.
  - **Research gap** — to support the claim that a transformer-only LIAR baseline is unlikely to generalise across datasets without explicit domain handling.
- The combination of PolitiFact + GossipCop + CoAID gives me a concrete reference for which datasets to include in my own cross-dataset experiments.

## 8) Risks / notes (simple)
- The full method depends on **social-media propagation graphs**, which are not part of LIAR (LIAR has only short statements + metadata, no Twitter data). So the *full* Silva framework cannot be directly applied to LIAR.
- For my project, I will use this paper as **motivation and conceptual baseline**, not as a system to reimplement end-to-end.
- The reported numbers (e.g. "7.55% F1 improvement") are for the cross-domain combined dataset, not for LIAR — they should not be quoted as a direct comparison to my LIAR results.
- The class balance across the three sub-datasets is very uneven, which interacts with the class-imbalance topic already discussed in my literature review.

## 9) LLM Prompt(s) Used
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
- If something is missing, write "Not mentioned".
- Use short bullet points for sections 3–8.
- If you make an inference, clearly label it as "Inference".
- Keep wording simple and clear.
