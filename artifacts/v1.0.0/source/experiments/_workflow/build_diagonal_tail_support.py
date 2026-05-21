#!/usr/bin/env python3
"""Build deterministic support rows for the v0.7 L1 diagonal tail-removal route."""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "src"))

from prime_clock_dynamics.experiments import write_csv, write_metadata
from prime_clock_dynamics.primes import primes_up_to


ARTIFACT_ID = "primeclock_dynamics_v0_7_diagonal_tail_removal"
DEFAULT_CASES = [
    (10_000, 2),
    (50_000, 3),
    (100_000, 4),
]


def slow_cutoff(window_size: int) -> int:
    """Return ``floor(N^(1/log log N))`` with a minimum prime-capable cutoff."""
    log_log = math.log(math.log(window_size))
    cutoff = int(window_size ** (1 / log_log))
    return max(2, cutoff)


def stable_float(value: float) -> str:
    """Return a stable text representation for CSV support floats."""
    return format(value, ".12g")


def variance_sum(prime_values: list[int]) -> float:
    """Return ``sum 1/p(1-1/p)`` as a proof-budget float."""
    return sum((1 / prime) * (1 - 1 / prime) for prime in prime_values)


def prime_harmonic_tail(prime_values: list[int], cutoff: int) -> float:
    """Return ``sum_{cutoff < p <= N} 1/p`` as a proof-budget float."""
    return sum(1 / prime for prime in prime_values if prime > cutoff)


def build_rows(cases: list[tuple[int, int]] | None = None) -> list[dict[str, object]]:
    """Return proof-budget rows for selected ``(N, k)`` cases."""
    rows: list[dict[str, object]] = []
    for window_size, moment_order in cases or DEFAULT_CASES:
        cutoff = slow_cutoff(window_size)
        dyadic_end = 2 * window_size
        cutoff_primes = primes_up_to(cutoff)
        dyadic_primes = primes_up_to(dyadic_end)
        cutoff_variance_float = variance_sum(cutoff_primes)
        dyadic_variance_float = variance_sum(dyadic_primes)
        tail_mean = prime_harmonic_tail(dyadic_primes, cutoff)
        log_log_window = math.log(math.log(window_size))
        theta = 1 / log_log_window
        budget_exponent = moment_order / log_log_window - 1
        normalized_budget = (
            len(cutoff_primes) ** moment_order
        ) / (window_size * (cutoff_variance_float ** (moment_order / 2)))
        dyadic_scale = math.sqrt(dyadic_variance_float)
        centering_gap = tail_mean
        scale_ratio = math.sqrt(cutoff_variance_float / dyadic_variance_float)
        rows.append(
            {
                "window_size": window_size,
                "dyadic_start": window_size + 1,
                "dyadic_end": dyadic_end,
                "moment_order": moment_order,
                "truncation": "floor(N^(1/loglogN))",
                "theta_fraction": "1/loglogN",
                "theta": stable_float(theta),
                "cutoff": cutoff,
                "cutoff_prime_count": len(cutoff_primes),
                "dyadic_prime_count": len(dyadic_primes),
                "cutoff_variance": stable_float(cutoff_variance_float),
                "dyadic_variance": stable_float(dyadic_variance_float),
                "dyadic_scale": stable_float(dyadic_scale),
                "loglog_window": stable_float(log_log_window),
                "cutoff_power_over_window": stable_float((cutoff**moment_order) / window_size),
                "cutoff_power_budget_exponent": stable_float(budget_exponent),
                "prime_count_power_over_window_variance_scale": stable_float(normalized_budget),
                "tail_prime_harmonic": stable_float(tail_mean),
                "tail_mean_over_dyadic_scale": stable_float(tail_mean / dyadic_scale),
                "centering_gap_A_2N_minus_A_y": stable_float(centering_gap),
                "centering_gap_over_dyadic_scale": stable_float(centering_gap / dyadic_scale),
                "scale_ratio_B_y_over_B_2N": stable_float(scale_ratio),
                "v0_6_y_power_budget_asymptotic": "for every fixed k, N^(k/loglogN-1) -> 0",
                "tail_l1_markov_target": "E[T_y]/B_2N -> 0",
                "uses_tail_moment_bound": False,
            }
        )
    return rows


def build_support(out_dir: Path, cases: list[tuple[int, int]] | None = None) -> dict[str, object]:
    """Write v0.7 support files and return the manifest."""
    out_dir.mkdir(parents=True, exist_ok=True)
    rows = build_rows(cases=cases)
    write_csv(out_dir / "diagonal_tail_support.csv", rows)
    manifest = {
        "artifact_id": ARTIFACT_ID,
        "support_status": "deterministic_v0_7_l1_diagonal_tail_support",
        "files": [
            "diagonal_tail_support.csv",
            "support_metadata.json",
        ],
        "row_count": len(rows),
    }
    (out_dir / "support_manifest.json").write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    write_metadata(
        out_dir / "support_metadata.json",
        {
            "artifact_id": ARTIFACT_ID,
            "note": "v0.7 diagonal tail support is deterministic proof-budget data, not statistical evidence.",
        },
    )
    return manifest


def parse_cases(value: str) -> list[tuple[int, int]]:
    """Parse comma-separated ``N:m`` cases."""
    cases: list[tuple[int, int]] = []
    for part in value.split(","):
        part = part.strip()
        if not part:
            continue
        pieces = part.split(":")
        if len(pieces) != 2:
            raise argparse.ArgumentTypeError("cases must use N:m entries")
        window_size, moment_order = (int(piece) for piece in pieces)
        if window_size < 2 or moment_order <= 0:
            raise argparse.ArgumentTypeError("cases require N>=2 and m>0")
        cases.append((window_size, moment_order))
    if not cases:
        raise argparse.ArgumentTypeError("at least one case is required")
    return cases


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out-dir", type=Path, required=True)
    parser.add_argument("--cases", type=parse_cases, default=DEFAULT_CASES)
    args = parser.parse_args()
    manifest = build_support(args.out_dir, cases=args.cases)
    print(
        "build_diagonal_tail_support: "
        f"files={len(manifest['files'])}, rows={manifest['row_count']}",
    )


if __name__ == "__main__":
    main()
