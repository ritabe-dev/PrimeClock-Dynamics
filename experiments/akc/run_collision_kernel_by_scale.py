#!/usr/bin/env python3
"""Build deterministic v1.1 collision-kernel support rows."""

from __future__ import annotations

import argparse
import csv
import math
from fractions import Fraction
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

from prime_clock_dynamics.collision_kernel import (  # noqa: E402
    collision_kernel,
    correlation_ratio,
    same_residue_prime_count,
)
from prime_clock_dynamics.multiplicity import multiplicity_covariance_baseline  # noqa: E402
from prime_clock_dynamics.primes import primes_up_to  # noqa: E402


def _fraction_from_float(value: float, denominator: int = 10**12) -> Fraction:
    return Fraction(round(value * denominator), denominator)


def build_rows() -> list[dict[str, object]]:
    """Return deterministic shrinking-angle kernel rows."""
    rows: list[dict[str, object]] = []
    base_alpha = Fraction(137, 1000)
    for cutoff in [100, 1000, 5000]:
        primes = primes_up_to(cutoff)
        log_x = math.log(cutoff)
        variance = multiplicity_covariance_baseline(base_alpha, base_alpha, primes)
        for theta in [0.25, 0.5, 0.75]:
            delta = math.exp(-(log_x**theta))
            beta = (base_alpha + _fraction_from_float(delta)) % 1
            kernel = collision_kernel(primes, base_alpha, beta)
            heuristic = math.log(math.log(min(cutoff, 1.0 / delta))) / math.log(math.log(cutoff))
            rows.append(
                {
                    "cutoff": cutoff,
                    "theta": theta,
                    "prime_count": len(primes),
                    "same_residue_prime_count": same_residue_prime_count(primes, base_alpha, beta),
                    "variance_B2": float(variance),
                    "collision_kernel": float(kernel),
                    "correlation_ratio": correlation_ratio(primes, base_alpha, beta),
                    "distance_heuristic_ratio": heuristic,
                    "status": "kernel_diagnostic",
                }
            )
    return rows


def write_csv(rows: list[dict[str, object]], out_path: Path) -> None:
    """Write rows to CSV."""
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    rows = build_rows()
    write_csv(rows, args.out)
    print(f"collision_kernel_by_scale: rows={len(rows)} out={args.out}")


if __name__ == "__main__":
    main()
