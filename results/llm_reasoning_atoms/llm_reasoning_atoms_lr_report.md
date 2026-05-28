# LLM-Generated Reasoning Atoms: TELLER-Like Experiment

- Date: 2026-05-25 13:45
- Feature cache: `results\llm_reasoning_atoms\llm_reasoning_atoms_features.jsonl`
- Decision model: `Logistic Regression`
- LLM is used only to generate structured reasoning signals; it does not directly predict REAL/FAKE.
- Label mapping: REAL=0, FAKE=1

## Atom Features

- `emotional_language`
- `exaggerated_claim`
- `specific_evidence`
- `source_reference`
- `logical_consistency`
- `clickbait_style`

## Compact Results

| target | model | train_n | test_n | accuracy | macro_f1 | real_recall | fake_recall | confusion_matrix |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| LIAR atoms -> LIAR | Logistic Regression | 400 | 200 | 0.6200 | 0.6198 | 0.6000 | 0.6400 | [[60, 40], [36, 64]] |
| LIAR atoms -> FakeNewsNet | Logistic Regression | 400 | 200 | 0.5300 | 0.4405 | 0.1300 | 0.9300 | [[13, 87], [7, 93]] |
| FakeNewsNet atoms -> FakeNewsNet | Logistic Regression | 200 | 200 | 0.6000 | 0.6000 | 0.5900 | 0.6100 | [[59, 41], [39, 61]] |

## Interpretation Notes

- `LIAR atoms -> LIAR` is the in-domain check.
- `LIAR atoms -> FakeNewsNet` is the cross-dataset transfer setting.
- `FakeNewsNet atoms -> FakeNewsNet` is the target-domain upper-bound check using the same atom feature space.
- This is a simplified TELLER-like setup: cognition-style atom generation is separated from the decision classifier.

## Classification Report: LIAR atoms -> LIAR

```text
precision    recall  f1-score   support

        REAL     0.6250    0.6000    0.6122       100
        FAKE     0.6154    0.6400    0.6275       100

    accuracy                         0.6200       200
   macro avg     0.6202    0.6200    0.6198       200
weighted avg     0.6202    0.6200    0.6198       200
```

## Classification Report: LIAR atoms -> FakeNewsNet

```text
precision    recall  f1-score   support

        REAL     0.6500    0.1300    0.2167       100
        FAKE     0.5167    0.9300    0.6643       100

    accuracy                         0.5300       200
   macro avg     0.5833    0.5300    0.4405       200
weighted avg     0.5833    0.5300    0.4405       200
```

## Classification Report: FakeNewsNet atoms -> FakeNewsNet

```text
precision    recall  f1-score   support

        REAL     0.6020    0.5900    0.5960       100
        FAKE     0.5980    0.6100    0.6040       100

    accuracy                         0.6000       200
   macro avg     0.6000    0.6000    0.6000       200
weighted avg     0.6000    0.6000    0.6000       200
```
