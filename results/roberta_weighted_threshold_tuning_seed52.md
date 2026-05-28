# Weighted RoBERTa Threshold Tuning (Seed 52)

- Date: 2026-04-11 22:36
- Model: `roberta-base` with weighted training loss
- Input: `statement` only
- Seed: `52`
- Thresholds scanned on validation: `0.30` to `0.70` in steps of `0.01`
- Best checkpoint still selected by validation macro-F1 at the default argmax classifier stage
- Threshold tuning is applied only after loading `best_state_dict`

## Comparison

| setting | threshold | best_epoch | valid_accuracy | valid_macro_f1 | valid_real_recall | valid_fake_recall | test_accuracy | test_macro_f1 | test_real_recall | test_fake_recall | test_confusion_matrix |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| default_0.50 | 0.5000 | 3 | 0.6604 | 0.6573 | 0.7260 | 0.5893 | 0.6606 | 0.6496 | 0.7437 | 0.5533 | [[531, 183], [247, 306]] |
| tuned_threshold | 0.5700 | 3 | 0.6706 | 0.6623 | 0.7949 | 0.5357 | 0.6582 | 0.6394 | 0.7871 | 0.4919 | [[562, 152], [281, 272]] |

## Top Validation Thresholds

| threshold | valid_accuracy | valid_macro_f1 | valid_real_recall | valid_fake_recall | valid_confusion_matrix |
| --- | --- | --- | --- | --- | --- |
| 0.5700 | 0.6706 | 0.6623 | 0.7949 | 0.5357 | [[531, 137], [286, 330]] |
| 0.5800 | 0.6713 | 0.6618 | 0.8069 | 0.5244 | [[539, 129], [293, 323]] |
| 0.5600 | 0.6682 | 0.6608 | 0.7844 | 0.5422 | [[524, 144], [282, 334]] |
| 0.5900 | 0.6706 | 0.6601 | 0.8129 | 0.5162 | [[543, 125], [298, 318]] |
| 0.6000 | 0.6706 | 0.6593 | 0.8189 | 0.5097 | [[547, 121], [302, 314]] |
| 0.4300 | 0.6597 | 0.6593 | 0.6662 | 0.6526 | [[445, 223], [214, 402]] |
| 0.5500 | 0.6659 | 0.6593 | 0.7740 | 0.5487 | [[517, 151], [278, 338]] |
| 0.5400 | 0.6651 | 0.6590 | 0.7680 | 0.5536 | [[513, 155], [275, 341]] |
| 0.5200 | 0.6628 | 0.6585 | 0.7440 | 0.5747 | [[497, 171], [262, 354]] |
| 0.5000 | 0.6604 | 0.6573 | 0.7260 | 0.5893 | [[485, 183], [253, 363]] |

## Interpretation

- Best validation threshold: `0.57`
The tuned threshold is higher than 0.50, so it makes the model more conservative about predicting FAKE.
- Test accuracy change vs 0.50: `-0.0024`
- Test macro-F1 change vs 0.50: `-0.0102`
- Test REAL recall change vs 0.50: `+0.0434`
- Test FAKE recall change vs 0.50: `-0.0615`
