from __future__ import annotations

import csv
from pathlib import Path

from scipy.stats import ttest_rel


ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "results"
OUT = RESULTS / "significance_tests" / "significance_tests_2026-07-02.csv"


def read_seed_metric(path: Path, metric: str, stage: str | None = None) -> dict[int, float]:
    rows: dict[int, float] = {}
    with path.open(newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            if stage is not None and row.get("stage") != stage:
                continue
            if row.get("section") and row["section"] != "per_seed":
                continue
            seed_text = (row.get("seed") or row.get("label") or "").replace("seed", "").strip()
            if not seed_text or seed_text.lower() in {"mean", "std"}:
                continue
            rows[int(seed_text)] = float(row[metric])
    return rows


def paired(name: str, a: dict[int, float], b: dict[int, float]) -> dict[str, str]:
    seeds = sorted(set(a) & set(b))
    av = [a[s] for s in seeds]
    bv = [b[s] for s in seeds]
    stat, p = ttest_rel(av, bv)
    return {
        "comparison": name,
        "metric": "macro_f1",
        "n": str(len(seeds)),
        "mean_a": f"{sum(av) / len(av):.4f}",
        "mean_b": f"{sum(bv) / len(bv):.4f}",
        "mean_diff_a_minus_b": f"{(sum(av) - sum(bv)) / len(av):.4f}",
        "t_statistic": f"{stat:.4f}",
        "p_value": f"{p:.6f}",
        "significant_p_lt_0_05": "yes" if p < 0.05 else "no",
        "test": "paired t-test, two-sided",
        "seeds": ",".join(map(str, seeds)),
    }


def main() -> None:
    in_domain = RESULTS / "in_domain_baselines"
    ft = RESULTS / "intermediate_finetuning"

    bert = read_seed_metric(in_domain / "bert_seed_sweep_results.csv", "test_macro_f1")
    wbert = read_seed_metric(in_domain / "bert_weighted_seed_sweep_results.csv", "test_macro_f1")
    wroberta = read_seed_metric(in_domain / "roberta_weighted_seed_sweep_results.csv", "test_macro_f1")

    direct = read_seed_metric(
        ft / "titles_only_direct_transfer_heldout_5seed_summary_20260530.csv",
        "macro_f1",
    )
    ft10 = read_seed_metric(
        ft / "intermediate_finetuning_weighted_roberta_seeds_42_52_62_72_82_fractions_0p10_full.csv",
        "macro_f1",
        "intermediate_ft",
    )
    ft20 = read_seed_metric(
        ft / "intermediate_finetuning_weighted_roberta_seeds_42_52_62_72_82_fractions_0p20_full.csv",
        "macro_f1",
        "intermediate_ft",
    )

    rows = [
        paired("LIAR weighted RoBERTa vs weighted BERT", wroberta, wbert),
        paired("LIAR weighted BERT vs unweighted BERT", wbert, bert),
        paired("LIAR weighted RoBERTa vs unweighted BERT", wroberta, bert),
        paired("FNN 10pct intermediate FT vs direct transfer", ft10, direct),
        paired("FNN 20pct intermediate FT vs direct transfer", ft20, direct),
        paired("FNN 20pct intermediate FT vs 10pct intermediate FT", ft20, ft10),
    ]

    OUT.parent.mkdir(parents=True, exist_ok=True)
    with OUT.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    print(OUT)


if __name__ == "__main__":
    main()
