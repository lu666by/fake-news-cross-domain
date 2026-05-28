## 1) Citation
- Suchin Gururangan, Ana Marasović, Swabha Swayamdipta, et al. *Don’t Stop Pretraining: Adapt Language Models to Domains and Tasks.* ACL 2020. doi:10.18653/v1/2020.acl-main.740 (arXiv:2004.10964)

## 2) One-sentence takeaway
If a pretrained language model (e.g., RoBERTa) is applied to a new domain, continuing masked language model (MLM) pretraining on unlabeled domain text (DAPT) and/or task text (TAPT) usually improves downstream classification performance.

## 3) What they propose (simple)
- **DAPT (Domain-Adaptive Pretraining):** Continue pretraining RoBERTa on a large unlabeled corpus from the target domain.
- **TAPT (Task-Adaptive Pretraining):** Continue pretraining only on the unlabeled task training text (smaller and cheaper).
- **DAPT + TAPT:** Apply both phases (often performs best).

## 4) What they tested
- Four domains (biomedical, computer science, news, reviews) and eight classification tasks (two per domain).
- Main research question: Does a second phase of pretraining help, even for strong pretrained models?

## 5) Evidence (beginner level, one example)
- The paper reports that DAPT consistently improves performance on tasks from the target domain when the model is not already in-domain.
- TAPT is much cheaper than DAPT and is often competitive.
- In many tasks, the results tables show the trend: RoBERTa < DAPT < TAPT / DAPT + TAPT (the best option varies by task).

## 6) Cost / practicality (important for MSc)
- DAPT can be compute-intensive because it uses large domain corpora and additional pretraining steps.
- TAPT uses only the task dataset text, making it less expensive while still providing meaningful gains.

## 7) How I will use it in my project (direct mapping)
- My setting: Train on dataset A (source) and test on dataset B (target) → domain mismatch.
- Practical idea: Before testing on target dataset B, continue pretraining on B’s unlabeled text to reduce sensitivity to writing style and vocabulary differences.
- This does not require additional labels, which makes it suitable for an MSc project.

## 8) Risks / notes (simple)
- If compute is limited, start with TAPT (cheaper) before attempting DAPT.
- Combining both phases may perform best but is also more expensive; experiments should remain small and controlled.

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
- If something is missing, write “Not mentioned”.
- Use short bullet points for sections 3–8.
- If you make an inference, clearly label it as “Inference”.
- Keep wording simple and clear.
