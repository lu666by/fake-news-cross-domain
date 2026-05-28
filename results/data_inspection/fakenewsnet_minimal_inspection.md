# FakeNewsNet Minimal Inspection

- Date: 2026-05-11 22:36
- Raw directory: `data\fakenewsnet_minimal\raw`
- Processed CSV: `data\fakenewsnet_minimal\processed\fakenewsnet_minimal_titles.csv`
- Text field used for modelling: `title` -> unified as `text`
- Label mapping: REAL=0, FAKE=1

## Basic Counts

- Total usable rows: `23196`
- Empty titles after cleaning: `0`
- Duplicate cleaned titles: `1472`

## Counts by Source and Label

| source | label_name | count |
| --- | --- | --- |
| gossipcop | FAKE | 5323 |
| gossipcop | REAL | 16817 |
| politifact | FAKE | 432 |
| politifact | REAL | 624 |

## Title Length Statistics

| source | label_name | char_len_count | char_len_mean | char_len_median | char_len_min | char_len_max | word_len_count | word_len_mean | word_len_median | word_len_min | word_len_max |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| gossipcop | FAKE | 5323 | 68.46 | 69.0 | 10 | 182 | 5323 | 11.06 | 11.0 | 1 | 31 |
| gossipcop | REAL | 16817 | 68.76 | 68.0 | 10 | 200 | 16817 | 11.3 | 11.0 | 1 | 39 |
| politifact | FAKE | 432 | 72.59 | 70.0 | 10 | 200 | 432 | 11.7 | 11.0 | 1 | 38 |
| politifact | REAL | 624 | 51.08 | 48.0 | 10 | 340 | 624 | 7.93 | 7.0 | 1 | 53 |

## Important Limitation

FakeNewsNet minimal contains `title`, not full article text. Therefore the cross-dataset experiment should be described as LIAR `statement` to FakeNewsNet `title` transfer.
