# Wang, Wang & Yang (2022) — Measure and Improve Robustness in NLP Models: A Survey

## 1) Citation
- Xuezhi Wang, Haohan Wang, Diyi Yang. “Measure and Improve Robustness in NLP Models: A Survey.” NAACL-HLT 2022. doi:10.18653/v1/2022.naacl-main.339

## 2) One-sentence takeaway
Robustness in NLP is mainly about how much performance drops when the test data differs from training (distribution shift) or when inputs are perturbed; strong in-domain scores do not guarantee robust generalisation.

## 3) Key definitions (in simple words)
- Robustness under distribution shift: test examples come from a different (naturally occurring) distribution; a model is robust if it does not degrade too much.
- “Natural” shifts can include: new datasets for the same task but from different domains, different speaker groups, dialects, etc.

## 4) Evaluation implications (what this means for my MSc)
- Reporting only in-domain results can be misleading, because the model may learn dataset-specific shortcuts.
- Cross-dataset evaluation (train on dataset A, test on dataset B) is a direct way to test robustness to natural distribution shift.
- The survey also distinguishes robustness without adaptation vs. domain adaptation; I can use this to clearly describe what I’m doing when I optionally add an adaptation step.

## 5) Why models fail (one key concept)
- Models often use “spurious correlations” (dataset bias / annotation artifacts): features that correlate with labels in one dataset but do not transfer to other datasets.

## 6) Mitigation strategies (only the categories I might use)
- Data-driven: better data coverage, augmentation, reweighting (reduce bias).
- Model-driven: training objectives or regularization to reduce reliance on spurious features; uncertainty estimation / ensembles.
- Inductive-prior-based: methods that bake in assumptions like invariance/causality (more advanced; probably not my first choice).

## 7) How this connects to my project
- It gives “theoretical legitimacy” for doing cross-dataset evaluation.
- It supports my motivation section: robustness to natural distribution shift is important for real deployment.
- It provides vocabulary for my thesis: distribution shift, OOD, spurious correlations, dataset bias.

## 8) Notes to reuse in proposal/introduction (short)
- In-domain accuracy ≠ robustness.
- Cross-dataset testing is a practical way to measure natural distribution shift robustness.
- Many failures are due to spurious correlations learned from dataset quirks.
