# Cross-Dataset Summary for Thesis

## Experiment Completed

The first strict cross-dataset experiment has been completed using the TF-IDF + Logistic Regression baseline.

Training setup:

- Source training data: LIAR train + validation splits
- Source test data: LIAR test split
- Target data: FakeNewsNet minimal titles
- Input setting: LIAR `statement` -> FakeNewsNet `title`
- Model: TF-IDF `(1,2)` + Logistic Regression
- No FakeNewsNet rows were used for training or tuning

## Main Result

| Target | N | Accuracy | Macro-F1 | REAL Recall | FAKE Recall |
| --- | ---: | ---: | ---: | ---: | ---: |
| LIAR test | 1,267 | 0.6235 | 0.6005 | 0.7661 | 0.4394 |
| FakeNewsNet PolitiFact titles | 1,056 | 0.5152 | 0.5146 | 0.4631 | 0.5903 |
| FakeNewsNet GossipCop titles | 22,140 | 0.4986 | 0.4715 | 0.4771 | 0.5664 |
| FakeNewsNet combined titles | 23,196 | 0.4993 | 0.4745 | 0.4766 | 0.5682 |

## Thesis Interpretation

This result can be used in the dissertation.

The main point is not that TF-IDF is a strong model. The main point is that a model which obtains reasonable in-domain performance on LIAR drops sharply when directly evaluated on FakeNewsNet titles. The LIAR test Macro-F1 is 0.6005, but the FakeNewsNet combined title Macro-F1 is only 0.4745. This supports the dissertation argument that in-domain performance does not guarantee cross-dataset reliability.

The result should be described carefully because FakeNewsNet minimal contains titles rather than full article text. Therefore, the experiment should be framed as short-text transfer from LIAR statements to FakeNewsNet titles, not full-article fake news detection.

## Suggested Thesis Wording

> As an initial strict cross-dataset baseline, the TF-IDF + Logistic Regression model was trained on the LIAR train and validation splits and evaluated directly on FakeNewsNet minimal titles. The model achieved 0.6235 Accuracy and 0.6005 Macro-F1 on the LIAR test split, but dropped to 0.4993 Accuracy and 0.4745 Macro-F1 on the combined FakeNewsNet title set. This result suggests that lexical patterns learned from LIAR political statements do not transfer reliably to FakeNewsNet titles, supporting the need for explicit cross-dataset evaluation rather than relying only on in-domain benchmark scores.

## Next Needed Result

The next result needed for the dissertation is a transformer cross-dataset pilot:

- weighted RoBERTa trained on LIAR
- evaluated on LIAR test
- evaluated directly on FakeNewsNet PolitiFact, GossipCop, and combined titles

This should be run only when CUDA/GPU is available, because current Python reports `torch.cuda.is_available() = False`.
