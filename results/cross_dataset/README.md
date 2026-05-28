# Cross-Dataset Results

This folder stores experiments where a model is trained on one dataset and evaluated on another dataset.

Current planned setting:

- Train on LIAR statement text.
- Evaluate directly on FakeNewsNet minimal title text.
- Do not use FakeNewsNet rows for training or checkpoint selection in strict transfer experiments.

Important terminology:

- **In-domain:** train and test on splits from the same dataset.
- **Strict cross-dataset transfer:** train on one dataset and test directly on another dataset.
- **FakeNewsNet minimal:** title-only CSV version from the official repository, not full article text.
