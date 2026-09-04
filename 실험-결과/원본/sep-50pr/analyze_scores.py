from __future__ import annotations

import json
import math
import random
import statistics
from pathlib import Path


HERE = Path(__file__).parent


def verdict(score: int) -> str:
    return "exact" if score == 4 else "partial" if score >= 2 else "miss"


def mcnemar(a: list[int], b: list[int]) -> dict:
    a_only = sum(x and not y for x, y in zip(a, b))
    b_only = sum(y and not x for x, y in zip(a, b))
    n = a_only + b_only
    tail = sum(math.comb(n, k) for k in range(min(a_only, b_only) + 1)) / 2**n if n else 1.0
    return {"qodo_only": a_only, "coderabbit_only": b_only, "two_sided_exact_p": min(1.0, 2 * tail)}


def wilson(successes: int, n: int, z: float = 1.959963984540054) -> list[float]:
    p = successes / n
    denominator = 1 + z * z / n
    center = (p + z * z / (2 * n)) / denominator
    half = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / denominator
    return [center - half, center + half]


def bootstrap_difference(a: list[int], b: list[int], rounds: int = 100_000) -> dict:
    rng = random.Random(20260904)
    n = len(a)
    samples = []
    for _ in range(rounds):
        indexes = [rng.randrange(n) for _ in range(n)]
        samples.append(sum(a[i] - b[i] for i in indexes) / n)
    samples.sort()
    return {
        "qodo_minus_coderabbit": sum(a) / n - sum(b) / n,
        "ci95_percentile": [samples[int(rounds * 0.025)], samples[int(rounds * 0.975) - 1]],
        "rounds": rounds,
        "seed": 20260904,
    }


def bootstrap_median_difference(a: list[float], b: list[float], rounds: int = 100_000) -> dict:
    rng = random.Random(20260904)
    n = len(a)
    samples = []
    for _ in range(rounds):
        indexes = [rng.randrange(n) for _ in range(n)]
        samples.append(statistics.median(a[i] for i in indexes) - statistics.median(b[i] for i in indexes))
    samples.sort()
    return {
        "qodo_minus_coderabbit_seconds": statistics.median(a) - statistics.median(b),
        "ci95_percentile_seconds": [samples[int(rounds * 0.025)], samples[int(rounds * 0.975) - 1]],
        "rounds": rounds,
        "seed": 20260904,
    }


def section(rows: list[dict]) -> dict:
    qodo = [row["qodo"] == 4 for row in rows]
    coderabbit = [row["coderabbit"] == 4 for row in rows]
    return {
        "n": len(rows),
        "qodo_exact": sum(qodo),
        "qodo_wilson_ci95": wilson(sum(qodo), len(rows)),
        "coderabbit_exact": sum(coderabbit),
        "coderabbit_wilson_ci95": wilson(sum(coderabbit), len(rows)),
        "mcnemar": mcnemar(qodo, coderabbit),
        "bootstrap": bootstrap_difference(qodo, coderabbit),
    }


def main() -> None:
    data = json.loads((HERE / "scores.json").read_text(encoding="utf-8"))
    if any(row["coderabbit"] is None for row in data["cases"]):
        raise SystemExit("CodeRabbit scores are incomplete")
    defects = [row for row in data["cases"] if row["kind"] == "defect"]
    defects_and_repeats = [row for row in data["cases"] if row["kind"] in {"defect", "repeat"}]
    controls = [row for row in data["cases"] if row["kind"] == "control"]
    blind = json.loads((HERE / "blind-findings.json").read_text(encoding="utf-8"))
    qodo_latency = [item["qodo"]["seconds"] for item in blind.values()]
    coderabbit_latency = [item["coderabbit"]["seconds"] for item in blind.values()]
    qodo_wall = [item["qodo"]["wall_seconds"] for item in blind.values()]
    coderabbit_wall = [item["coderabbit"]["wall_seconds"] for item in blind.values()]
    if any(value is None for value in qodo_latency + coderabbit_latency + qodo_wall + coderabbit_wall):
        raise SystemExit("Review timing is incomplete")
    result = {
        "new_defects": section(defects),
        "new_defects_and_repeats": section(defects_and_repeats),
        "controls": {
            product: {"false_positives": sum(row[product] > 0 for row in controls), "n": len(controls)}
            for product in ("qodo", "coderabbit")
        },
        "latency_seconds": {
            product: {
                "n": len(values),
                "median": statistics.median(values),
                "min": min(values),
                "max": max(values),
            }
            for product in ("qodo", "coderabbit")
            if (values := [item[product]["seconds"] for item in blind.values() if item[product]["seconds"] is not None])
        },
        "paired_median_latency": bootstrap_median_difference(qodo_latency, coderabbit_latency),
        "wall_latency_seconds": {
            "qodo": {"median": statistics.median(qodo_wall), "min": min(qodo_wall), "max": max(qodo_wall)},
            "coderabbit": {"median": statistics.median(coderabbit_wall), "min": min(coderabbit_wall), "max": max(coderabbit_wall)},
        },
        "paired_median_wall_latency": bootstrap_median_difference(qodo_wall, coderabbit_wall),
        "verdict_counts": {
            product: {
                label: sum(verdict(row[product]) == label for row in defects_and_repeats)
                for label in ("exact", "partial", "miss")
            }
            for product in ("qodo", "coderabbit")
        },
        "patches": {
            product: {
                "offered": sum(item["product"] == product for item in data["patches"]),
                "fully_fixed": sum(item["product"] == product and item["verdict"] == "fully_fixed" for item in data["patches"]),
            }
            for product in ("qodo", "coderabbit")
        },
    }
    (HERE / "statistics.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, indent=2))


def self_check() -> None:
    assert mcnemar([1, 1, 0, 0], [1, 0, 1, 0]) == {"qodo_only": 1, "coderabbit_only": 1, "two_sided_exact_p": 1.0}
    assert wilson(0, 10)[0] == 0.0
    assert bootstrap_difference([1], [0], 100)["ci95_percentile"] == [1.0, 1.0]
    assert bootstrap_median_difference([2], [5], 100)["ci95_percentile_seconds"] == [-3, -3]


if __name__ == "__main__":
    self_check()
    main()
