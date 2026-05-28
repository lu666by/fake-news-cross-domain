# Liu et al. (2024) — TELLER

## 1. Citation

Liu, H., Wang, W., Li, H., & Li, H. (2024). TELLER: A Trustworthy Framework for Explainable, Generalizable and Controllable Fake News Detection. *Findings of ACL 2024*.

arXiv: https://arxiv.org/abs/2402.07776
Code: https://github.com/less-and-less-bugs/Trust_TELLER

---

## 2. One-sentence takeaway

TELLER is a two-system fake news detection framework that uses human-defined logic predicates to guide an LLM in generating logic atoms, then learns logic rules to aggregate them — designed for explainability, generalisation, and controllability beyond standard fine-tuned classifiers.

---

## 3. What problem does it address?

Existing deep-learning-based fake news detectors (including BERT/RoBERTa fine-tuned classifiers) have three limitations:

- **Not explainable**: the reasoning process is a black box.
- **Poor generalisation**: they often fail on out-of-domain data.
- **LLM integration risk**: directly using LLMs without constraints is unpredictable.

TELLER tries to address all three at the same time.

---

## 4. What is TELLER?

TELLER has two main systems:

**Cognition system:**
- Uses human-defined *logical predicates* (structured feature templates, e.g. "contains a numeric claim", "attributed to a named source") to guide the LLM.
- The LLM generates human-readable *logic atoms* for each input — symbolic facts about the claim.

**Decision system:**
- Learns *logic rules* that aggregate the atoms.
- The rules are used to predict the truthfulness label.
- Because the rules are explicit and symbolic, the decision process is interpretable.

In short: TELLER is not a simple text classifier. It is a hybrid symbolic + neural system where an LLM does feature extraction (atoms) and a rule learner does classification.

---

## 5. How is it different from BERT / RoBERTa?

| | BERT / RoBERTa (my baseline) | TELLER |
|---|---|---|
| Input processing | Fine-tuned on raw text | LLM generates logic atoms from text |
| Classification | Neural softmax head | Logic rule aggregation |
| Explainability | Low | High (explicit symbolic rules) |
| LLM required? | No | Yes (OpenAI API) |
| Generalisation design | Not specifically designed | Explicitly targets cross-domain |
| Reproducibility | Easy (HuggingFace) | Requires OpenAI API key + setup |

---

## 6. What datasets and results are reported?

The paper evaluates on four datasets. LIAR binary is explicitly supported (the repo contains `drive_liar.py` for in-domain and `drive_dg.py` for cross-domain experiments).

**Reported LIAR binary results (from paper):**
- Accuracy: `0.6773`
- Macro-F1: `0.6697`

These are higher than my weighted RoBERTa baseline (`0.6522` / `0.6396`), but TELLER is a significantly more complex system that requires an LLM backend.

---

## 7. Cost / feasibility for my MSc project

**Key bottleneck: OpenAI API required.**

- The GitHub README explicitly states: "Place your OpenAI key into the file named `api_key.txt`."
- No local LLM alternative (Llama-2, Mistral, etc.) is mentioned.
- Every run sends claim text to the OpenAI API — which has per-token cost and rate limits.
- On LIAR (10,240 train + 1,267 test), the LLM call cost could be significant and unpredictable.

**Other constraints:**
- The codebase is small (11 Python scripts), so it is readable, but the logic atom generation step and rule learning are harder to debug than a standard HuggingFace fine-tuning loop.
- No GPU memory requirements stated — logic rule learning is likely CPU-based, but the LLM calls are API-based.
- Human-defined predicates require expert knowledge to design; they are not automatically generated.

**Conclusion:** Reproduction is limited by OpenAI API cost and dependency, not by local GPU. This makes full reproduction non-trivial within a typical MSc student budget.

---

## 8. How I can use it in my dissertation

1. **Advanced literature comparison**: include TELLER in the LIAR comparison table as a published result. Mark as `Partly comparable` — it uses a fundamentally different framework.
2. **Literature review**: discuss in Section 3 (LLM / reasoning-based fake news detection) as a representative 2024 work showing the direction beyond fine-tuned classifiers.
3. **Research gap**: note that TELLER requires an LLM API and human-defined predicates, which limits accessibility and reproducibility. My approach focuses on locally trainable transformer baselines without external API dependencies.
4. **Future work**: if OpenAI API access is available, running TELLER on the same binary LIAR split would provide a direct comparison point.

---

## 9. Risks / notes

- I have not run TELLER myself. All numbers above (`0.6773` / `0.6697`) are from the published paper.
- The OpenAI API dependency means results could vary if the underlying model version changes (GPT-4 vs GPT-3.5, etc.).
- The paper does not specify which OpenAI model is used — this affects reproducibility and cost estimation.
- The logic predicate design involves human expertise; it is not a fully automated pipeline.
- Do NOT write "I will run TELLER" in the dissertation at this stage. Correct framing: "TELLER is included as an advanced literature comparison; full reproduction is outside the scope of this MSc project due to API cost and system complexity."

---

## 10. LLM Prompts Used

- WebFetch arXiv abstract page (2025-05-09): extracted framework description, venue, authors, code link.
- WebFetch GitHub README (2025-05-09): extracted LLM dependency (OpenAI API), dataset support (`drive_liar.py`), and run instructions.
