# LLM-Generated Reasoning Atoms Experiment Plan

This experiment is a lightweight TELLER-like pilot: an LLM generates structured cognition-style atoms, and a separate classifier makes the REAL/FAKE decision.

**Fixed positioning:** this is an exploratory pilot, not the main contribution of the dissertation. It should be used as supporting evidence about the limits of LLM-generated reasoning signals under domain shift, while the main contribution remains the reproducible class-sensitive baseline and cross-dataset generalisation study.

## Features

- `emotional_language`
- `exaggerated_claim`
- `specific_evidence`
- `source_reference`
- `logical_consistency`
- `clickbait_style`
- `reason` is saved for auditability but is not used as a classifier input.

## Experiments

| Experiment | Training | Testing | Purpose |
|---|---|---|---|
| LIAR atoms -> LIAR | LIAR train+valid atom features | LIAR test atom features | In-domain check |
| LIAR atoms -> FakeNewsNet | LIAR train+valid atom features | FakeNewsNet test atom features | Cross-dataset transfer |
| FakeNewsNet atoms -> FakeNewsNet | FakeNewsNet train atom features | FakeNewsNet test atom features | Target-domain upper bound |

## Suggested Pilot

Start with a balanced small sample before full annotation:

```powershell
python notebooks/12_llm_reasoning_atoms_teller_like.py generate --provider deepseek --model deepseek-v4-flash --max-per-group 20
python notebooks/12_llm_reasoning_atoms_teller_like.py train --model-type lr
```

Use `--provider openai --model gpt-4o-mini` or `--provider ollama --model <local-model>` as alternatives.
