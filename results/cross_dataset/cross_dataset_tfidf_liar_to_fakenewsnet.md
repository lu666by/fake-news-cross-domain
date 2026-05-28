# Cross-Dataset TF-IDF: LIAR to FakeNewsNet Minimal

- Date: 2026-05-11 22:36
- Final training data: LIAR train + validation splits after selecting the existing TF-IDF V2 configuration
- Source test: LIAR test split
- Target dataset: FakeNewsNet minimal titles
- Input transfer setting: LIAR `statement` -> FakeNewsNet `title`
- Model: TF-IDF `(1,2)` + Logistic Regression
- TF-IDF fit only on LIAR train + validation text
- No FakeNewsNet rows used for training or tuning

## Compact Results

| target | n | accuracy | macro_f1 | real_recall | fake_recall | confusion_matrix |
| --- | --- | --- | --- | --- | --- | --- |
| LIAR test | 1267 | 0.6235 | 0.6005 | 0.7661 | 0.4394 | [[547, 167], [310, 243]] |
| FakeNewsNet PolitiFact titles | 1056 | 0.5152 | 0.5146 | 0.4631 | 0.5903 | [[289, 335], [177, 255]] |
| FakeNewsNet GossipCop titles | 22140 | 0.4986 | 0.4715 | 0.4771 | 0.5664 | [[8023, 8794], [2308, 3015]] |
| FakeNewsNet combined titles | 23196 | 0.4993 | 0.4745 | 0.4766 | 0.5682 | [[8312, 9129], [2485, 3270]] |

## Interpretation

- This is the first strict cross-dataset baseline in the project.
- The model is trained only on LIAR and directly evaluated on FakeNewsNet titles.
- The FakeNewsNet minimal target is title-only, so results should not be described as full-article fake news detection.
- A large performance drop from LIAR to FakeNewsNet would support the dissertation argument that in-domain performance does not guarantee cross-dataset reliability.

## Classification Report: LIAR test

```text
precision    recall  f1-score   support

        REAL     0.6383    0.7661    0.6964       714
        FAKE     0.5927    0.4394    0.5047       553

    accuracy                         0.6235      1267
   macro avg     0.6155    0.6028    0.6005      1267
weighted avg     0.6184    0.6235    0.6127      1267
```

## Classification Report: FakeNewsNet PolitiFact titles

```text
precision    recall  f1-score   support

        REAL     0.6202    0.4631    0.5303       624
        FAKE     0.4322    0.5903    0.4990       432

    accuracy                         0.5152      1056
   macro avg     0.5262    0.5267    0.5146      1056
weighted avg     0.5433    0.5152    0.5175      1056
```

## Classification Report: FakeNewsNet GossipCop titles

```text
precision    recall  f1-score   support

        REAL     0.7766    0.4771    0.5911     16817
        FAKE     0.2553    0.5664    0.3520      5323

    accuracy                         0.4986     22140
   macro avg     0.5160    0.5217    0.4715     22140
weighted avg     0.6513    0.4986    0.5336     22140
```

## Classification Report: FakeNewsNet combined titles

```text
precision    recall  f1-score   support

        REAL     0.7698    0.4766    0.5887     17441
        FAKE     0.2637    0.5682    0.3603      5755

    accuracy                         0.4993     23196
   macro avg     0.5168    0.5224    0.4745     23196
weighted avg     0.6443    0.4993    0.5320     23196
```
