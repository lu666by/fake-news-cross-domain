# Gururangan et al. (2020) — Don’t Stop Pretraining: Adapt Language Models to Domains and Tasks

## 1) Citation
- Suchin Gururangan, Ana Marasović, Swabha Swayamdipta, et al. “Don’t Stop Pretraining: Adapt Language Models to Domains and Tasks.” ACL 2020. doi:10.18653/v1/2020.acl-main.740 (arXiv:2004.10964)

## 2) One-sentence takeaway
If a pretrained LM (like RoBERTa) is used on a new domain, continuing masked-LM pretraining on unlabeled domain text (DAPT) and/or task text (TAPT) usually improves downstream classification performance.

## 3) What they propose (simple)
- DAPT (Domain-Adaptive Pretraining): continue pretraining RoBERTa on a large unlabeled corpus from the target domain.
- TAPT (Task-Adaptive Pretraining): continue pretraining only on the unlabeled task training text (smaller, cheaper).
- DAPT + TAPT: do both (often best).

## 4) What they tested
- 4 domains (biomedical, computer science, news, reviews) and 8 classification tasks (2 per domain).
- Main question: does a second phase of pretraining help, even for strong pretrained models?

## 5) Evidence (keep it beginner-level, one example is enough)
- They report DAPT “consistently improves performance” on tasks from the target domain (when target is not already in-domain for RoBERTa).
- TAPT is much cheaper than DAPT and is often competitive.
- In their table of results, RoBERTa < DAPT < TAPT / DAPT+TAPT for many tasks (exact best varies by task).

## 6) Cost / practicality (important for MSc)
- DAPT can be compute-heavy because it uses large domain corpora and more pretraining steps.
- TAPT uses only the task dataset text and is therefore much less expensive; it can still give solid gains.

## 7) How I will use it in my project (very direct mapping)
- My setting: Train on dataset A (source) but test on dataset B (target) → domain mismatch.
- Practical idea: Before testing on target dataset B, continue pretraining on B’s unlabeled text to reduce sensitivity to B’s writing style/vocabulary.
- This does NOT require additional labels, which makes it suitable for an MSc project.

## 8) Risks / notes (simple)
- If compute is limited, start with TAPT (cheaper) before attempting DAPT.
- Combining phases may be best but also most expensive; keep experiments small and controlled.
