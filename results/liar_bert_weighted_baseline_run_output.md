# LIAR BERT Weighted-Loss Run Output

- Date: 2026-04-08 15:26
- Task: Binary classification
- Input field: statement
- Label mapping: REAL=0, FAKE=1
- Model: bert-base-uncased
- Max length: 128
- Epochs: 3
- Learning rate: 2e-05

## Class weights from train split
- REAL (0): 0.8901
- FAKE (1): 1.1408

## Best validation checkpoint
- Epoch: 2
- Validation Accuracy: 0.6425
- Validation Macro-F1: 0.6407

## Final weighted BERT test result
- Accuracy: 0.6456
- Macro-F1: 0.6380

## Training history

| epoch | train_loss | train_accuracy | train_macro_f1 | valid_loss | valid_accuracy | valid_macro_f1 |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 0.6770 | 0.5708 | 0.5707 | 0.6501 | 0.6207 | 0.6196 |
| 2 | 0.6079 | 0.6707 | 0.6686 | 0.6369 | 0.6425 | 0.6407 |
| 3 | 0.4697 | 0.7828 | 0.7803 | 0.7079 | 0.6347 | 0.6283 |

## Confusion matrix
- Label order: [0, 1] = [REAL, FAKE]
```
[[501 213]
 [236 317]]
```

## Classification report
```
              precision    recall  f1-score   support

        REAL     0.6798    0.7017    0.6906       714
        FAKE     0.5981    0.5732    0.5854       553

    accuracy                         0.6456      1267
   macro avg     0.6389    0.6375    0.6380      1267
weighted avg     0.6441    0.6456    0.6447      1267

```