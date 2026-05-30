# TELLER-Like 1000-Row Pilot Positioning Note

- Date: 2026-05-30
- Decision: keep the 1000-row reasoning-atoms experiment as an exploratory pilot only.

## Why Not Treat It as a Strong Result

The current cache contains one 1000-row sample generated with DeepSeek V4 Flash:

- LIAR train REAL/FAKE: 100 + 100
- LIAR valid REAL/FAKE: 100 + 100
- LIAR test REAL/FAKE: 100 + 100
- FakeNewsNet train REAL/FAKE: 100 + 100
- FakeNewsNet test REAL/FAKE: 100 + 100

This is useful as a small feasibility check, but it is not enough to support a strong claim about TELLER-like reasoning atoms in general. The supervisor's concern is valid: one random sample can make the result look better or worse than a different 1000-row sample.

A second practical limitation is that the current shell does not have `DEEPSEEK_API_KEY` or `OPENAI_API_KEY` configured, so new independent LLM annotation samples cannot be generated immediately. The current script also writes to a single fixed cache path, so repeated samples would need isolated work directories or a cache-path argument to avoid mixing samples.

## Thesis Wording

Use cautious wording:

> A small exploratory TELLER-inspired reasoning-atoms pilot was also conducted. It separates LLM-generated reasoning signals from the final decision model, but it is not a full reproduction of TELLER and is not treated as a main contribution. In the current DeepSeek V4 Flash 1000-row setup, atom features contain some signal in-domain, but the setup has limited performance under cross-dataset transfer. Because this pilot uses a single limited sample, it should be interpreted as supporting evidence only.

Avoid strong wording:

- Do not say "TELLER-like methods fail."
- Do not say "LLM reasoning atoms do not work."
- Do not say "LLMs are not suitable for fake news detection."
- Do not compare the pilot directly against the main transformer experiments as if it were equally validated.

## If More Time Becomes Available

The next reliability check would be to generate separate 1000-row caches for multiple seeds, such as 42, 52, and 62, then report mean/std for the three atom-classifier experiments. Each cache should be isolated so one sample does not contaminate another.
