## 10) Literature comparison on LIAR

### More directly comparable LIAR results

| Source | Setting | Model | Accuracy | Macro-F1 | Comparable? | Note |
|---|---|---|---:|---:|---|---|
| This project | LIAR binary | TF-IDF + Logistic Regression | 0.6235 | 0.6005 | Yes | Main sparse baseline |
| This project | LIAR binary | BERT-base (5-run mean) | 0.6425 ± 0.0095 | 0.6231 ± 0.0122 | Yes | Main unweighted neural baseline |
| This project | LIAR binary | BERT-base + weighted loss (5-run mean) | 0.6412 ± 0.0065 | 0.6322 ± 0.0090 | Yes | Stronger FAKE recall |
| This project | LIAR binary | RoBERTa-base + weighted loss (5-run mean) | 0.6522 ± 0.0074 | 0.6396 ± 0.0080 | Yes | Current strongest overall model |
| Liu et al. (2024) TELLER | LIAR binary | TELLER | 67.73 | 66.97 | Yes | Stronger than the current baselines, but uses a more advanced framework |
| Papageorgiou et al. (2025) | LIAR binary / multi-dataset evaluation | BERT-based classifier | 0.63 | 0.64* | Partly | Uses multiple datasets; not the same as strict cross-dataset transfer |

\* Reported as F1-score in the paper summary; not explicitly stated there as macro-F1.

### Background-only LIAR reference (not directly comparable)

| Source | Setting | Model | Accuracy | Comparable? | Note |
|---|---|---|---:|---|---|
| Wang (2017) | LIAR original 6-way setup | Hybrid CNN | 0.274 | No | Original LIAR benchmark paper; useful as dataset background rather than a direct comparison to the current binary setup |

### Interpretation

The current weighted RoBERTa result is clearly stronger than the sparse baseline and also stronger than the current unweighted BERT line. Compared with recent LIAR binary work, it is still below the stronger result reported by TELLER, which suggests that the current project has established a solid neural baseline line but has not yet reached more advanced framework-level performance. The Wang (2017) LIAR paper is useful mainly as dataset background because it uses the original 6-way setup rather than the binary setting used in this project.
