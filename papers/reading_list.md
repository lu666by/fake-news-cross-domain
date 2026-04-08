# Reading List (living document)

Legend: ToRead / Reading / Done (skim) / Done (full)

| Priority | Paper | Year | Topic | Why relevant | Status | Summary file |
|---|---|---:|---|---|---|---|
| P0 | Wang (2017) — LIAR dataset | 2017 | Dataset / Claims | Core dataset paper; defines the LIAR benchmark, labels, and short political-claim setting | Done (skim) | `summaries/wang2017_liar.md` |
| P0 | Devlin et al. (2019) — BERT | 2019 | Transformer / Method | Core method paper for using BERT as a baseline model in this project | Done (skim) | `summaries/devlin2019_bert.md` |
| P0 | Gururangan et al. (2020) — Don’t Stop Pretraining (DAPT/TAPT) | 2020 | Domain adaptation | Important for later cross-domain / cross-dataset discussion and lightweight adaptation ideas | Done (skim) | `summaries/gururangan2020_dapt.md` |
| P0 | Wang, Wang & Yang (2022) — Robustness Survey | 2022 | Robustness / OOD | Defines robustness and motivates OOD / cross-dataset evaluation | Done (skim) | `summaries/wang2022_robustness_survey.md` |
| P0 | Papageorgiou et al. (2025) — Harnessing Large Language Models and Deep Neural Networks for Fake News Detection | 2025 | Fake news detection / Cross-dataset | Directly relevant to LIAR, fake news detection, transformer baselines, and cross-dataset generalisation | Done (skim) | `summaries/papageorgiou_2025_llm_fake_news.md` |

## Current reading focus

The current reading focus is now split into three parts:

1. **dataset and task background**
   - LIAR dataset paper
   - fake news detection benchmark papers

2. **model and method justification**
   - BERT / transformer baseline papers
   - domain adaptation papers
   - robustness / OOD papers

3. **next-stage cross-dataset motivation**
   - papers that discuss generalisation gaps across datasets
   - papers that compare performance across multiple fake news datasets

## Next candidates (to add)

- [ ] FakeNewsNet dataset paper
- [ ] one stronger LIAR binary baseline paper for direct result comparison
- [ ] one additional cross-dataset fake news generalisation paper
- [ ] one paper focused on error analysis / interpretability in misinformation detection

## Notes

- This file is only the reading index.
- Detailed notes should be written in `papers/summaries/`.
- Once a paper is read, its status here should be updated and the summary file should be added immediately.
- The literature review now needs to move beyond the earlier 3-paper stage and better match the current experimental progress.
