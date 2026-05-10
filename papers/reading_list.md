# Reading List

**Project:** Cross-dataset Generalisation for Fake News Detection  
**Last updated:** 2026-05-10

---

## Legend

- **Priority:** P0 = must read before next meeting / P1 = read within 2 weeks / P2 = reference as needed
- **Status:** Done / Reading / To-read
- **Section:** Which lit review section this paper belongs to

---

## Existing papers (already have summaries)

| Priority | Paper | Year | Section | Notes | Status | Summary file |
|----------|-------|------|---------|-------|--------|--------------|
| P0 | Wang (2017) — LIAR Dataset | 2017 | §1 Datasets | Foundational dataset paper; 6-class LIAR; background for binary mapping | Done | `summaries/wang2017_liar.md` |
| P0 | Devlin et al. (2019) — BERT | 2019 | §2 Transformer-based | Foundation model for all my baselines | Done | `summaries/devlin2019_bert.md` |
| P0 | Gururangan et al. (2020) — DAPT | 2020 | §5 Cross-domain | Domain-adaptive pretraining; relevant to cross-domain generalisation | Done | `summaries/gururangan2020_dapt.md` |
| P0 | Wang et al. (2022) — Robustness survey | 2022 | §5 Cross-domain | Survey of robustness in fake news detection; distribution shift | Done | `summaries/wang2022_robustness_survey.md` |
| P0 | Papageorgiou et al. (2025) — LLM + fake news | 2025 | §2 & §3 | Multi-dataset evaluation (NOT strict cross-dataset transfer) | Done | `summaries/papageorgiou_2025_llm_fake_news.md` |
| P0 | Henning et al. (2023) — Class imbalance survey | 2023 | §4 Class imbalance | Survey of class imbalance methods in NLP | Done | `summaries/henning2023_class_imbalance_survey.md` |
| P0 | Liu et al. (2024) — TELLER | 2024 | §3 LLM/reasoning | Advanced fake news framework; feasibility investigated; LIAR 0.6773/0.6697 | Done | `summaries/liu2024_teller.md` |

---

## Second-round additions (2026-05-10) — summaries written

| Priority | Paper | Year | Section | Notes | Status | Summary file |
|----------|-------|------|---------|-------|--------|--------------|
| P0 | Liu et al. (2019) — RoBERTa | 2019 | §2 Transformer-based | Direct foundation for weighted RoBERTa baseline; shows BERT undertrained | Done | `summaries/liu2019_roberta.md` |
| P0 | Shu et al. (2020) — FakeNewsNet | 2020 | §1 Datasets | Second most used fake news dataset after LIAR; cross-dataset candidate | Done | `summaries/shu2020_fakenewsnet.md` |
| P1 | Silva et al. (2021) — Embracing Domain Differences | 2021 | §5 Cross-domain | Cross-domain fake news; tackles domain shift explicitly; AAAI 2021 | Done | `summaries/silva2021_cross_domain_fake_news.md` |
| P1 | Hu et al. (2024) — Bad Actor, Good Advisor | 2024 | §3 LLM/reasoning | LLM influence on fake news generation and detection; dual role of LLMs | Done | `summaries/hu2024_bad_actor_good_advisor.md` |

## Still to-read

| Priority | Paper | Year | Section | Notes | Status | Summary file |
|----------|-------|------|---------|-------|--------|--------------|
| P1 | Augenstein et al. (2019) — MultiFC | 2019 | §1 Datasets | Multi-source fact verification; 26 fact-checking websites; EMNLP 2019 | To-read | — |
| P1 | Castelo et al. (2019) — Topic-agnostic features | 2019 | §5 Cross-domain | Domain-invariant features for fake news; opposite design choice to Silva 2021 | To-read | — |
| P1 | Han et al. (2020) — Continual learning for fake news | 2020 | §5 Cross-domain | Frames cross-domain detection as continual learning; EWC + GEM | To-read | — |
| P1 | Pelrine et al. (2023) — LLM prompting for fake news | 2023 | §3 LLM/reasoning | Systematic LLM prompting comparison; LLM alone underperforms fine-tuned SLM | To-read | — |
| P2 | Pan et al. (2023) — Program-guided Reasoning | 2023 | §3 LLM/reasoning | Fact-checking with program-guided reasoning; reasoning-based approach; ACL 2023 | To-read | — |
| P2 | Rashkin et al. (2017) — Truth of Varying Shades | 2017 | §2 Traditional | Early linguistic baseline for fake news detection | To-read | — |

---

## Notes

- **TELLER feasibility:** See `results/teller_feasibility_note.md`. Requires OpenAI API; not feasible to reproduce in full within MSc project. Use as advanced literature comparison only.
- **Papageorgiou 2025:** Mark as multi-dataset evaluation (NOT strict cross-dataset transfer).
- **LIAR binary mapping:** REAL = {true, mostly-true, half-true}, FAKE = {barely-true, false, pants-fire}.
- **Do NOT** add papers just to pad the count. Each paper should appear in the lit review with a specific contribution mentioned.
