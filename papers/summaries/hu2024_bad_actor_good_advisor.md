# Hu et al. (2024) — *Bad Actor, Good Advisor: Exploring the Role of Large Language Models in Fake News Detection*

## 1) Citation
- Beizhe Hu, Qiang Sheng, Juan Cao, Yuhui Shi, Yang Li, Danding Wang, Peng Qi. *Bad Actor, Good Advisor: Exploring the Role of Large Language Models in Fake News Detection.* AAAI 2024. (arXiv:2309.12247)

## 2) One-sentence takeaway
Hu et al. show that GPT-3.5 by itself underperforms a fine-tuned BERT for fake news detection, but that LLM-generated rationales — when used as advice for a small fine-tuned model rather than as the predictor — produce a stronger system than either model alone.

## 3) What they propose (simple)
- **Empirical finding (the "Bad Actor" half):** prompting GPT-3.5 directly to predict fake / real news is consistently worse than fine-tuning BERT on the same task, across four prompting strategies (zero-shot, zero-shot CoT, few-shot, few-shot CoT).
- **Diagnostic finding:** the LLM is **good at producing multi-perspective rationales** (textual description, commonsense, factuality) but **bad at integrating them into a final judgement**. Factuality reasoning specifically suffers from hallucination.
- **Method (the "Good Advisor" half) — ARG (Adaptive Rationale Guidance):** keep the SLM (BERT) as the actual classifier, and let the LLM provide rationales as side input. The SLM learns to **selectively absorb** useful rationales rather than blindly trust them.
- **ARG-D:** a distilled, rationale-free version of ARG. At inference time it does not need to query the LLM — useful when API cost matters.

## 4) What they tested
- **Datasets:**
  - **Weibo21** (Chinese): ~5K train / ~2K val / ~2K test
  - **GossipCop** (English): ~3.9K train / ~1.3K val / ~1.3K test
- **Models compared:**
  - GPT-3.5-turbo with 4 prompting strategies (zero-shot, zero-shot CoT, few-shot, few-shot CoT)
  - Fine-tuned BERT (chinese-bert-wwm-ext / bert-base-uncased)
  - SLM-only baselines, LLM-only baselines, and SLM+LLM combination baselines
- **Metric:** macro-F1.

## 5) Evidence (beginner level, one example)
- Best LLM result vs fine-tuned BERT (Table 2):
  - Chinese: GPT-3.5 best = 0.725 (few-shot), BERT = **0.753** (+3.8%)
  - English: GPT-3.5 best = 0.702 (few-shot CoT), BERT = **0.765** (+9.0%)
- Per-perspective analysis (Table 3): commonsense and textual-description rationales reach macro-F1 ≈ 0.70, but factuality drops to ~0.63 due to hallucination.
- Oracle voting over the LLM's perspective-specific judgements reaches **0.908 (Chinese) / 0.878 (English)**, showing the rationales contain enough signal — the bottleneck is **integration**, not analysis.
- ARG and ARG-D outperform all three baseline categories (SLM-only, LLM-only, SLM+LLM combinations) on both datasets.

## 6) Cost / practicality (important for MSc)
- Querying GPT-3.5 for rationales requires the **OpenAI API** — same blocker as TELLER. Each training example needs at least one API call to obtain its rationale.
- For an MSc project on a single GPU and a free-tier API budget, **full ARG reproduction is not feasible** on LIAR's 10,240 training claims.
- However, **ARG-D (the distilled, rationale-free version)** is conceptually the more practical direction for an MSc project: at inference time it is just a fine-tuned SLM, with the LLM only needed during training-data generation.
- Even ARG-D still requires the API once at training time, so direct reproduction is unlikely to fit my budget.

## 7) How I will use it in my project (direct mapping)
- This is one of the core **2024 references** the supervisor specifically asked me to add. It belongs in the **"LLM and reasoning-based fake news detection"** section of my literature review.
- It complements TELLER: where TELLER uses LLM-generated logic atoms as part of a structured framework, Hu et al. use LLM rationales as soft advice to an SLM. Citing both gives a fuller picture of how 2024 work integrates LLMs with smaller models.
- The "LLM as advisor, not predictor" framing is a useful **interpretive lens** for the discussion section: my own results show fine-tuned RoBERTa (an SLM) beating naive LLM-style approaches, which is consistent with their finding.
- The paper supports the conservative MSc-scope decision to keep my main system as a fine-tuned BERT/RoBERTa and only refer to LLM-based work as literature comparison.

## 8) Risks / notes (simple)
- The numbers in this paper are for **Weibo21 / GossipCop**, not LIAR — they cannot be quoted as a direct baseline against my LIAR results.
- Macro-F1 for fine-tuned BERT on GossipCop here (0.765) is much higher than on LIAR (around 0.62–0.64 in my experiments). This is consistent with LIAR being a harder, shorter-text dataset, but the comparison should be made carefully in the thesis.
- The paper is from 2024 and the API landscape has shifted since publication. Reproducing exact API behaviour today (with newer GPT-3.5-turbo or GPT-4o snapshots) may give somewhat different numbers.
- ARG itself is non-trivial to implement; for the literature review, the framing-level takeaway ("LLM as advisor not predictor") is more useful than the architectural details.

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
