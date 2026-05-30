# Intermediate Fine-Tuning Experiment

Main follow-up experiment after direct LIAR -> FakeNewsNet transfer.

Protocol:

1. Train source model on LIAR train.
2. Select source checkpoint by LIAR validation Macro-F1.
3. Continue fine-tuning on a small balanced labeled subset of FakeNewsNet train titles.
4. Select intermediate checkpoint by FakeNewsNet validation Macro-F1.
5. Evaluate once on held-out FakeNewsNet test titles.

Default pilot command:

```powershell
python notebooks/13_intermediate_finetuning_fakenewsnet.py --model-key weighted_roberta --seeds 42 --target-fractions 0.01,0.05,0.10
```

This experiment is intended as the main practical response to the weak direct cross-dataset transfer baseline.
