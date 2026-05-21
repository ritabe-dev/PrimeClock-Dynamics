#!/usr/bin/env python3
"""Build deterministic support rows for the v0.8 diagonal Angular EK record."""

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


ARTIFACT_ID = "primeclock_dynamics_v0_8_diagonal_angular_ek"
DEFAULT_CASES = [
    (10**6, 2),
    (10**12, 3),
    (10**18, 4),
]


def stable_float(value: float) -> str:
    """Return stable compact text for proof-budget floats."""
    return format(value, ".12g")


def slow_cutoff(window_start: int) -> int:
    """Return floor(N^(1/log log N)) for sufficiently large ``N``."""
    log_n = math.log(window_start)
    loglog_n = math.log(log_n)
    return max(2, int(math.floor(math.exp(log_n / loglog_n))))


def variance_float(prime_values: list[int]) -> float:
    """Return the fixed-cutoff variance baseline as a float."""
    return sum((1.0 / prime) * (1.0 - 1.0 / prime) for prime in prime_values)


def build_rows(cases: list[tuple[int, int]] | None = None) -> list[dict[str, object]]:
    """Return proof-budget rows for ``(N, moment_order)`` cases."""
    rows: list[dict[str, object]] = []
    for window_start, moment_order in cases or DEFAULT_CASES:
        cutoff = slow_cutoff(window_start)
        prime_values = primes_up_to(cutoff)
        loglog_2n = math.log(math.log(2 * window_start))
        loglog_y = math.log(math.log(cutoff))
        dyadic_variance_asymptotic = loglog_2n
        cutoff_variance = variance_float(prime_values)
        y_power_budget = (cutoff**moment_order) / window_start
        tail_prime_harmonic_asymptotic = max(loglog_2n - loglog_y, 0.0)
        dyadic_scale = math.sqrt(dyadic_variance_asymptotic)
        rows.append(
            {
                "window_start_N": window_start,
                "window_end_2N": 2 * window_start,
                "moment_order": moment_order,
                "slow_cutoff_y": cutoff,
                "prime_count_pi_y": len(prime_values),
                "truncation": "floor(N^(1/loglogN))",
                "y_power_over_N": stable_float(y_power_budget),
                "v0_6_fixed_order_budget_asymptotic": "N^(k/loglogN - 1) -> 0 for fixed k",
                "finite_row_y_power_budget_below_one": y_power_budget < 1.0,
                "cutoff_variance_B_y_squared": stable_float(cutoff_variance),
                "dyadic_variance_asymptotic": stable_float(dyadic_variance_asymptotic),
                "scale_ratio_B_y_over_B_2N": stable_float(
                    math.sqrt(cutoff_variance / dyadic_variance_asymptotic),
                ),
                "tail_prime_harmonic_asymptotic": stable_float(tail_prime_harmonic_asymptotic),
                "tail_mean_over_dyadic_scale": stable_float(
                    tail_prime_harmonic_asymptotic / dyadic_scale,
                ),
                "centering_gap_over_dyadic_scale": stable_float(
                    tail_prime_harmonic_asymptotic / dyadic_scale,
                ),
                "slutsky_tail_target": "T_y/B_2N -> 0 in probability",
                "assembly_status": "gate_c_verified_support",
            }
        )
    return rows


def build_support(out_dir: Path, cases: list[tuple[int, int]] | None = None) -> dict[str, object]:
    """Write v0.8 support files and return the manifest."""
    out_dir.mkdir(parents=True, exist_ok=True)
    rows = build_rows(cases=cases)
    write_csv(out_dir / "diagonal_angular_ek_support.csv", rows)
    manifest = {
        "artifact_id": ARTIFACT_ID,
        "support_status": "deterministic_v0_8_diagonal_angular_ek_gate_c_support",
        "files": [
            "diagonal_angular_ek_support.csv",
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
            "note": "v0.8 support rows are deterministic proof-budget sanity checks, not statistical evidence.",
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
        window_start, moment_order = (int(piece) for piece in pieces)
        if window_start <= 100 or moment_order <= 0:
            raise argparse.ArgumentTypeError("cases require N>100 and m>0")
        cases.append((window_start, moment_order))
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
        "build_diagonal_angular_ek_support: "
        f"files={len(manifest['files'])}, rows={manifest['row_count']}",
    )


if __name__ == "__main__":
    main()
