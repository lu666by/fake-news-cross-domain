# LIAR vs FakeNewsNet Dataset-Shift Analysis

- Date: 2026-05-30
- Purpose: explain why LIAR -> FakeNewsNet transfer is difficult and why title-only evaluation can behave differently from longer/full-text settings.
- Important data limitation: FakeNewsNet Minimal contains titles only; article body text is unavailable in the local dataset. Therefore, the main comparison is LIAR `statement` text vs FakeNewsNet `title` text.

## Length Summary

| dataset     | text_type   | label   |   rows |   char_mean |   char_median |   char_p90 |   word_mean |   word_median |   word_p90 | body_available   |
|:------------|:------------|:--------|-------:|------------:|--------------:|-----------:|------------:|--------------:|-----------:|:-----------------|
| LIAR        | statement   | FAKE    |   5657 |      104.04 |            95 |        164 |       17.42 |            16 |         28 | True             |
| LIAR        | statement   | REAL    |   7134 |      109.63 |           101 |        169 |       18.54 |            17 |         29 | True             |
| FakeNewsNet | title       | FAKE    |   5755 |       68.77 |            69 |         96 |       11.11 |            11 |         16 | False            |
| FakeNewsNet | title       | REAL    |  17441 |       68.13 |            68 |         96 |       11.18 |            11 |         16 | False            |

## Vocabulary Overlap

| vocab_scope   |   liar_vocab |   fakenewsnet_vocab |   overlap |   jaccard |   fnn_terms_seen_in_liar_pct |   liar_terms_seen_in_fnn_pct |
|:--------------|-------------:|--------------------:|----------:|----------:|-----------------------------:|-----------------------------:|
| top_100       |          100 |                 100 |        10 |    0.0526 |                        10    |                        10    |
| top_250       |          250 |                 250 |        29 |    0.0616 |                        11.6  |                        11.6  |
| top_500       |          500 |                 500 |        94 |    0.1038 |                        18.8  |                        18.8  |
| top_1000      |         1000 |                1000 |       248 |    0.1416 |                        24.8  |                        24.8  |
| top_2000      |         2000 |                2000 |       608 |    0.1792 |                        30.4  |                        30.4  |
| all_terms     |        12550 |               17836 |      6211 |    0.2569 |                        34.82 |                        49.49 |

## Dataset-Distinctive Terms

| comparison          | term         |   LIAR_count |   FakeNewsNet_count | direction   |   log_odds_abs |
|:--------------------|:-------------|-------------:|--------------------:|:------------|---------------:|
| LIAR vs FakeNewsNet | percent      |         1505 |                   6 | LIAR        |          5.696 |
| LIAR vs FakeNewsNet | unemployment |          208 |                   0 | LIAR        |          5.658 |
| LIAR vs FakeNewsNet | dont         |          206 |                   0 | LIAR        |          5.649 |
| LIAR vs FakeNewsNet | wisconsin    |          331 |                   1 | LIAR        |          5.429 |
| LIAR vs FakeNewsNet | weve         |          143 |                   0 | LIAR        |          5.285 |
| LIAR vs FakeNewsNet | thats        |          126 |                   0 | LIAR        |          5.16  |
| LIAR vs FakeNewsNet | rhode        |          124 |                   0 | LIAR        |          5.144 |
| LIAR vs FakeNewsNet | legislation  |          116 |                   0 | LIAR        |          5.078 |
| LIAR vs FakeNewsNet | rate         |          323 |                   2 | LIAR        |          4.999 |
| LIAR vs FakeNewsNet | businesses   |          102 |                   0 | LIAR        |          4.95  |
| LIAR vs FakeNewsNet | sector       |          100 |                   0 | LIAR        |          4.93  |
| LIAR vs FakeNewsNet | theres       |           96 |                   0 | LIAR        |          4.89  |
| LIAR vs FakeNewsNet | voted        |          447 |                   4 | LIAR        |          4.813 |
| LIAR vs FakeNewsNet | taxpayer     |           87 |                   0 | LIAR        |          4.792 |
| LIAR vs FakeNewsNet | nations      |           85 |                   0 | LIAR        |          4.769 |
| LIAR vs FakeNewsNet | trillion     |          164 |                   1 | LIAR        |          4.728 |
| LIAR vs FakeNewsNet | doesnt       |           81 |                   0 | LIAR        |          4.722 |
| LIAR vs FakeNewsNet | gov          |          242 |                   2 | LIAR        |          4.711 |
| LIAR vs FakeNewsNet | combined     |           79 |                   0 | LIAR        |          4.697 |
| LIAR vs FakeNewsNet | taxes        |          444 |                   5 | LIAR        |          4.624 |
| LIAR vs FakeNewsNet | elected      |           69 |                   0 | LIAR        |          4.563 |
| LIAR vs FakeNewsNet | increase     |          201 |                   2 | LIAR        |          4.526 |
| LIAR vs FakeNewsNet | revenue      |           66 |                   0 | LIAR        |          4.52  |
| LIAR vs FakeNewsNet | teachers     |           66 |                   0 | LIAR        |          4.52  |
| LIAR vs FakeNewsNet | rates        |          129 |                   1 | LIAR        |          4.49  |
| LIAR vs FakeNewsNet | kardashian   |            0 |                1073 | FakeNewsNet |          6.67  |
| LIAR vs FakeNewsNet | awards       |            0 |                 634 | FakeNewsNet |          6.142 |
| LIAR vs FakeNewsNet | meghan       |            0 |                 585 | FakeNewsNet |          6.062 |
| LIAR vs FakeNewsNet | reveals      |            0 |                 475 | FakeNewsNet |          5.853 |
| LIAR vs FakeNewsNet | selena       |            0 |                 456 | FakeNewsNet |          5.812 |

## Label-Distinctive Terms

| dataset     | comparison   | term          |   FAKE_count |   REAL_count | direction   |   log_odds_abs |
|:------------|:-------------|:--------------|-------------:|-------------:|:------------|---------------:|
| LIAR        | FAKE vs REAL | socialists    |           10 |            0 | FAKE        |          2.609 |
| LIAR        | FAKE vs REAL | betty         |            9 |            0 | FAKE        |          2.514 |
| LIAR        | FAKE vs REAL | sean          |            9 |            0 | FAKE        |          2.514 |
| LIAR        | FAKE vs REAL | takeover      |           18 |            1 | FAKE        |          2.462 |
| LIAR        | FAKE vs REAL | duffy         |            8 |            0 | FAKE        |          2.408 |
| LIAR        | FAKE vs REAL | sutton        |            8 |            0 | FAKE        |          2.408 |
| LIAR        | FAKE vs REAL | corruption    |            8 |            0 | FAKE        |          2.408 |
| LIAR        | FAKE vs REAL | scheme        |           16 |            1 | FAKE        |          2.351 |
| LIAR        | FAKE vs REAL | deciding      |           16 |            1 | FAKE        |          2.351 |
| LIAR        | FAKE vs REAL | options       |            6 |            0 | FAKE        |          2.157 |
| LIAR        | FAKE vs REAL | protest       |            6 |            0 | FAKE        |          2.157 |
| LIAR        | FAKE vs REAL | thank         |            6 |            0 | FAKE        |          2.157 |
| LIAR        | FAKE vs REAL | slush         |            6 |            0 | FAKE        |          2.157 |
| LIAR        | FAKE vs REAL | debunked      |            6 |            0 | FAKE        |          2.157 |
| LIAR        | FAKE vs REAL | bulbs         |           12 |            1 | FAKE        |          2.083 |
| LIAR        | FAKE vs REAL | incarceration |            0 |           12 | REAL        |          2.354 |
| LIAR        | FAKE vs REAL | losses        |            0 |           11 | REAL        |          2.274 |
| LIAR        | FAKE vs REAL | february      |            0 |           10 | REAL        |          2.187 |
| LIAR        | FAKE vs REAL | richest       |            1 |           18 | REAL        |          2.041 |
| LIAR        | FAKE vs REAL | gunfire       |            0 |            8 | REAL        |          1.986 |
| LIAR        | FAKE vs REAL | torture       |            0 |            8 | REAL        |          1.986 |
| LIAR        | FAKE vs REAL | attorneys     |            0 |            8 | REAL        |          1.986 |
| LIAR        | FAKE vs REAL | capacity      |            0 |            8 | REAL        |          1.986 |
| LIAR        | FAKE vs REAL | huckabee      |            0 |            8 | REAL        |          1.986 |
| LIAR        | FAKE vs REAL | wade          |            0 |            8 | REAL        |          1.986 |
| LIAR        | FAKE vs REAL | buono         |            0 |            8 | REAL        |          1.986 |
| LIAR        | FAKE vs REAL | accidents     |            1 |           15 | REAL        |          1.869 |
| LIAR        | FAKE vs REAL | retiree       |            0 |            7 | REAL        |          1.869 |
| LIAR        | FAKE vs REAL | defended      |            0 |            7 | REAL        |          1.869 |
| LIAR        | FAKE vs REAL | generate      |            0 |            7 | REAL        |          1.869 |
| FakeNewsNet | FAKE vs REAL | hollywoodlife |           23 |            0 | FAKE        |          4.058 |
| FakeNewsNet | FAKE vs REAL | elope         |           12 |            0 | FAKE        |          3.444 |
| FakeNewsNet | FAKE vs REAL | jealousy      |           11 |            0 | FAKE        |          3.364 |
| FakeNewsNet | FAKE vs REAL | dump          |           10 |            0 | FAKE        |          3.277 |
| FakeNewsNet | FAKE vs REAL | enquirer      |           10 |            0 | FAKE        |          3.277 |
| FakeNewsNet | FAKE vs REAL | muslim        |            9 |            0 | FAKE        |          3.182 |
| FakeNewsNet | FAKE vs REAL | keanu         |            8 |            0 | FAKE        |          3.076 |
| FakeNewsNet | FAKE vs REAL | rumor         |           33 |            3 | FAKE        |          3.02  |
| FakeNewsNet | FAKE vs REAL | neri          |           23 |            2 | FAKE        |          2.959 |
| FakeNewsNet | FAKE vs REAL | debunked      |           23 |            2 | FAKE        |          2.959 |

## Thesis-Ready Interpretation

LIAR and FakeNewsNet Minimal differ not only in label source but also in text form. LIAR examples are short fact-checking statements, while the available FakeNewsNet Minimal target data consists of news titles. This means that the transfer experiment is a statement-to-title transfer setting rather than full-article fake-news detection.

The length analysis shows that both datasets are short-text settings, but their distributions and lexical signals are not identical. FakeNewsNet titles contain outlet/topic/headline vocabulary, whereas LIAR statements contain political-claim vocabulary and fact-checking-style phrasing. This helps explain why a model trained on LIAR can preserve a strong FAKE bias when moved to FakeNewsNet: it learns source-domain lexical and stylistic cues that do not map cleanly onto the target title domain.

The vocabulary-overlap table shows limited overlap even among high-frequency terms. This supports the interpretation that cross-dataset failure is driven by domain and style shift, not simply by model weakness. Title-only evaluation may sometimes look slightly different from longer-text settings because titles are short, selective, and headline-like; they may remove some article-body noise, but they also amplify style and topic mismatch.

These analyses should be used as explanatory evidence, not as predictive features. Their role is to justify the dissertation's interpretation: strict LIAR -> FakeNewsNet transfer is hard because the target data changes both the domain and the text genre, and intermediate target-domain fine-tuning helps because it exposes the model to target-title vocabulary and label associations.

## Generated Figures

- `figures/word_length_by_dataset_label.png`
- `figures/fake_top_terms_by_dataset.png`
- `figures/vocabulary_overlap_topn.png`
- `figures/dataset_distinctive_terms.png`
