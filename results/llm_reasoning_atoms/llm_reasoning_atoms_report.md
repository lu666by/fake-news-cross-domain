# LLM-Generated Reasoning Atoms: TELLER-Like Experiment

- Date: 2026-05-25 12:40
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
| LIAR atoms -> LIAR | Logistic Regression | 80 | 40 | 0.5750 | 0.5747 | 0.6000 | 0.5500 | [[12, 8], [9, 11]] |
| LIAR atoms -> FakeNewsNet | Logistic Regression | 80 | 40 | 0.5500 | 0.4872 | 0.2000 | 0.9000 | [[4, 16], [2, 18]] |
| FakeNewsNet atoms -> FakeNewsNet | Logistic Regression | 40 | 40 | 0.5000 | 0.4885 | 0.6500 | 0.3500 | [[13, 7], [13, 7]] |

## Interpretation Notes

- `LIAR atoms -> LIAR` is the in-domain check.
- `LIAR atoms -> FakeNewsNet` is the cross-dataset transfer setting.
- `FakeNewsNet atoms -> FakeNewsNet` is the target-domain upper-bound check using the same atom feature space.
- This is a simplified TELLER-like setup: cognition-style atom generation is separated from the decision classifier.

## Classification Report: LIAR atoms -> LIAR

```text
precision    recall  f1-score   support

        REAL     0.5714    0.6000    0.5854        20
        FAKE     0.5789    0.5500    0.5641        20

    accuracy                         0.5750        40
   macro avg     0.5752    0.5750    0.5747        40
weighted avg     0.5752    0.5750    0.5747        40
```

## Classification Report: LIAR atoms -> FakeNewsNet

```text
precision    recall  f1-score   support

        REAL     0.6667    0.2000    0.3077        20
        FAKE     0.5294    0.9000    0.6667        20

    accuracy                         0.5500        40
   macro avg     0.5980    0.5500    0.4872        40
weighted avg     0.5980    0.5500    0.4872        40
```

## Classification Report: FakeNewsNet atoms -> FakeNewsNet

```text
precision    recall  f1-score   support

        REAL     0.5000    0.6500    0.5652        20
        FAKE     0.5000    0.3500    0.4118        20

    accuracy                         0.5000        40
   macro avg     0.5000    0.5000    0.4885        40
weighted avg     0.5000    0.5000    0.4885        40
```
