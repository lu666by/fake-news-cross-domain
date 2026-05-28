# LLM-Generated Reasoning Atoms: TELLER-Like Experiment

- Date: 2026-05-25 13:45
- Feature cache: `results\llm_reasoning_atoms\llm_reasoning_atoms_features.jsonl`
- Decision model: `Random Forest`
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
| LIAR atoms -> LIAR | Random Forest | 400 | 200 | 0.6050 | 0.6049 | 0.6200 | 0.5900 | [[62, 38], [41, 59]] |
| LIAR atoms -> FakeNewsNet | Random Forest | 400 | 200 | 0.5300 | 0.4686 | 0.1900 | 0.8700 | [[19, 81], [13, 87]] |
| FakeNewsNet atoms -> FakeNewsNet | Random Forest | 200 | 200 | 0.6000 | 0.5998 | 0.5800 | 0.6200 | [[58, 42], [38, 62]] |

## Interpretation Notes

- `LIAR atoms -> LIAR` is the in-domain check.
- `LIAR atoms -> FakeNewsNet` is the cross-dataset transfer setting.
- `FakeNewsNet atoms -> FakeNewsNet` is the target-domain upper-bound check using the same atom feature space.
- This is a simplified TELLER-like setup: cognition-style atom generation is separated from the decision classifier.

## Classification Report: LIAR atoms -> LIAR

```text
precision    recall  f1-score   support

        REAL     0.6019    0.6200    0.6108       100
        FAKE     0.6082    0.5900    0.5990       100

    accuracy                         0.6050       200
   macro avg     0.6051    0.6050    0.6049       200
weighted avg     0.6051    0.6050    0.6049       200
```

## Classification Report: LIAR atoms -> FakeNewsNet

```text
precision    recall  f1-score   support

        REAL     0.5938    0.1900    0.2879       100
        FAKE     0.5179    0.8700    0.6493       100

    accuracy                         0.5300       200
   macro avg     0.5558    0.5300    0.4686       200
weighted avg     0.5558    0.5300    0.4686       200
```

## Classification Report: FakeNewsNet atoms -> FakeNewsNet

```text
precision    recall  f1-score   support

        REAL     0.6042    0.5800    0.5918       100
        FAKE     0.5962    0.6200    0.6078       100

    accuracy                         0.6000       200
   macro avg     0.6002    0.6000    0.5998       200
weighted avg     0.6002    0.6000    0.5998       200
```
