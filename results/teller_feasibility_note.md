# TELLER Feasibility Note

**Date:** 2026-05-09
**Purpose:** Answer the supervisor's question: "Can you use TELLER? If not, why not?"
**Reference:** Liu et al. (2024), Findings of ACL 2024. Code: https://github.com/less-and-less-bugs/Trust_TELLER

---

## 1. What is TELLER?

TELLER (Liu et al., 2024) is a fake news detection framework published at Findings of ACL 2024. It is not a simple fine-tuned transformer classifier. Instead, it is a dual-system framework combining:

- **A cognition system**: uses human-defined logical predicates to prompt an LLM, which then generates symbolic *logic atoms* — structured, human-readable facts about the input claim.
- **A decision system**: learns generalizable *logic rules* that aggregate the atoms and predict the truthfulness label.

The key idea is to make fake news detection more explainable, more generalisable across domains, and more controllable compared to black-box neural classifiers.

---

## 2. How is it different from BERT / RoBERTa?

My current baselines (BERT, RoBERTa) are fine-tuned text classifiers: they take a claim as input and produce a label directly via a softmax layer. The reasoning is implicit — it happens inside the neural network weights and is not interpretable.

TELLER is fundamentally different:
- It does not fine-tune a transformer on the raw text.
- It uses an **LLM (via OpenAI API)** to convert the input claim into structured symbolic atoms.
- It then learns **explicit logic rules** from these atoms to make predictions.

This means TELLER requires an additional component (an LLM) and an additional abstraction layer (logic atoms + rules) that my BERT/RoBERTa baselines do not have.

---

## 3. What data / input does it need?

- **Input**: claim text (statement), same as my LIAR binary setup. TELLER's `drive_liar.py` is designed for the LIAR dataset directly.
- **Extra requirement**: the claim text is sent to the OpenAI API to generate logic atoms. This step is not local — it requires an active OpenAI API connection.
- **Human-defined predicates**: the logic predicates used to guide the LLM are designed by hand. They encode domain knowledge (e.g., "does the claim contain a specific number?", "is there a named source?"). These are not automatically generated and may need to be adapted for different datasets.

---

## 4. Is code available?

Yes. The official code is at: https://github.com/less-and-less-bugs/Trust_TELLER

The repository structure:
- `drive_liar.py` — in-domain experiments (LIAR dataset)
- `drive_dg.py` — cross-domain generalisation experiments
- `models/` and `utils/` directories
- ~11 Python scripts total; also shell scripts for pipeline steps

The code is publicly available and the dataset can be downloaded from OneDrive as per the README.

---

## 5. Can it be reproduced in this MSc project?

**Partially feasible, but with a significant blocker.**

| Factor | Status |
|--------|--------|
| Code is available | ✅ Yes (GitHub) |
| LIAR dataset supported | ✅ Yes (`drive_liar.py`) |
| Local GPU required | ✅ Not for the LLM step |
| OpenAI API required | ❌ Yes — hard dependency |
| API cost for full LIAR run | ❌ Unknown but potentially high (10,240 training samples) |
| Human-defined predicates needed | ⚠️ Yes — requires reading and understanding the predicate design |
| Time to understand + adapt | ⚠️ Moderate — more complex than HuggingFace fine-tuning |

The primary blocker is the **OpenAI API dependency**. Every claim in the dataset must be sent to the OpenAI API to generate logic atoms. The cost of doing this for 10,240 training samples + 1,267 test samples is not specified in the paper or README.

---

## 6. If not fully feasible, why not?

Three concrete reasons:

**Reason 1 — API cost and dependency:**
TELLER requires an active OpenAI API key for every run. Running it on the full LIAR binary dataset (train + test) involves thousands of API calls. For an MSc project without a dedicated API budget, this is a practical constraint that is difficult to work around without code changes.

**Reason 2 — System complexity:**
TELLER is a multi-component pipeline (LLM atom generation → logic rule learning → classification) rather than a single fine-tuning loop. Debugging, adapting, or extending it requires understanding multiple systems at once. This is a higher barrier than adapting a HuggingFace model.

**Reason 3 — Predicate design:**
The logic predicates that guide the LLM are hand-crafted by domain experts. Reproducing TELLER faithfully means using the same predicates, or redesigning them — both require a clear understanding of the original predicate engineering decisions, which are not fully documented in the public code.

---

## 7. How I will use it in this dissertation

**Current plan (feasibility investigation stage):**

1. **Advanced literature comparison**: TELLER is included in the LIAR binary results table (`liar_baseline.md`, Section 10) as a published result. It is marked as `Partly comparable` because it is a different type of system — not a direct BERT/RoBERTa baseline.

2. **Literature review (Section 3 — LLM/reasoning-based fake news detection)**: TELLER is discussed as a representative 2024 paper showing the direction beyond simple fine-tuned classifiers. Its contribution (dual-system, explainable, cross-domain) and limitation (OpenAI API dependency, complex setup) are both noted.

3. **Research gap**: The API dependency and system complexity of TELLER support the argument that there is value in studying simpler, locally reproducible baselines — which is what my weighted BERT and weighted RoBERTa models represent.

4. **If time and API access permit**: Running TELLER on the same LIAR binary split would produce a directly comparable result. This is noted as possible future work, but not a current commitment.

**Summary sentence for supervisor:**
TELLER is useful as an advanced literature comparison. Full reproduction within this MSc project is not currently feasible due to OpenAI API cost and system complexity, but it is included as a published benchmark result and discussed in the literature review.

---

*My current best model (weighted RoBERTa): Accuracy `0.6522`, Macro-F1 `0.6396`*
*TELLER reported result: Accuracy `0.6773`, Macro-F1 `0.6697` (Liu et al., 2024)*
