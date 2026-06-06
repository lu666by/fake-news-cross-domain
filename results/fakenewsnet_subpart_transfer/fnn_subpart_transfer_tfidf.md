# Within-FakeNewsNet Subpart Transfer (TF-IDF + weighted LR)

- Date: 2026-06-05
- PolitiFact: n=1056 REAL=624 FAKE=432
- GossipCop: n=22140 REAL=16817 FAKE=5323
- Model: TF-IDF (1-2 gram, min_df=2, sublinear) + class-weighted Logistic Regression.
- Binary REAL(0)/FAKE(1), title text only. In-domain rows are 5-seed 80/20 mean; transfer rows are deterministic (all source -> all target).

| Setting | Train->Test | n_train | n_test | Accuracy | Macro-F1 | REAL recall | FAKE recall |
|---|---|---:|---:|---:|---:|---:|---:|
| In-domain PolitiFact (5-seed 80/20) | PolitiFact->PolitiFact | 844 | 211 | 0.8377 (±0.029) | 0.8329 (±0.031) | 0.8512 | 0.8184 |
| In-domain GossipCop (5-seed 80/20) | GossipCop->GossipCop | 17712 | 4428 | 0.8311 (±0.005) | 0.7814 (±0.005) | 0.8609 | 0.7369 |
| Transfer PolitiFact -> GossipCop | PolitiFact->GossipCop | 1056 | 22140 | 0.4244 | 0.4185 | 0.3457 | 0.6729 |
| Transfer GossipCop -> PolitiFact | GossipCop->PolitiFact | 22140 | 1056 | 0.6193 | 0.5411 | 0.8734 | 0.2523 |