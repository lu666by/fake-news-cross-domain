# Within-FakeNewsNet Subpart Transfer (weighted RoBERTa, seed 42)

- Date: 2026-06-06 10:04
- Model: roberta-base, class-weighted, max_len 128, batch 16, 3 epochs, checkpoint by valid Macro-F1.
- Single seed (42); title text only; REAL(0)/FAKE(1). In-domain = 64/16/20 split; transfer = train all source -> test all target.
- Total runtime: 29.3 min.

| Setting | Accuracy | Macro-F1 | REAL recall | FAKE recall |
|---|---:|---:|---:|---:|
| In-domain PolitiFact | 0.9245 | 0.9205 | 0.9760 | 0.8506 |
| In-domain GossipCop | 0.8437 | 0.7962 | 0.8733 | 0.7502 |
| Transfer PolitiFact -> GossipCop | 0.3018 | 0.2860 | 0.1007 | 0.9371 |
| Transfer GossipCop -> PolitiFact | 0.4725 | 0.4722 | 0.3798 | 0.6065 |