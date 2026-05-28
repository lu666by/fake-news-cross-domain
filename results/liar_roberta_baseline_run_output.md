# LIAR RoBERTa Baseline Run Output

- Date: 2026-04-08 16:02
- Task: Binary classification
- Input field: statement
- Label mapping: REAL=0, FAKE=1
- Model: roberta-base
- Max length: 128
- Epochs: 3
- Learning rate: 2e-05
- TF-IDF V2 Accuracy reference: 0.6235
- TF-IDF V2 Macro-F1 reference: 0.6005

## Best validation checkpoint
- Epoch: 3
- Validation Accuracy: 0.6558
- Validation Macro-F1: 0.6435

## Final BERT test result
- Accuracy: 0.6504
- Macro-F1: 0.6262
- Accuracy delta vs TF-IDF V2: +0.0269
- Macro-F1 delta vs TF-IDF V2: +0.0257

## Training history

| epoch | train_loss | train_accuracy | train_macro_f1 | valid_loss | valid_accuracy | valid_macro_f1 |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 0.6697 | 0.5883 | 0.5526 | 0.6526 | 0.6316 | 0.6253 |
| 2 | 0.6226 | 0.6591 | 0.6506 | 0.6441 | 0.6503 | 0.6319 |
| 3 | 0.5419 | 0.7363 | 0.7297 | 0.6720 | 0.6558 | 0.6435 |

## Confusion matrix
- Label order: [0, 1] = [REAL, FAKE]
```
[[573 141]
 [302 251]]
```

## Classification report
```
              precision    recall  f1-score   support

        REAL     0.6549    0.8025    0.7212       714
        FAKE     0.6403    0.4539    0.5312       553

    accuracy                         0.6504      1267
   macro avg     0.6476    0.6282    0.6262      1267
weighted avg     0.6485    0.6504    0.6383      1267

```
