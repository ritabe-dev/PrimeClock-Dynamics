#!/usr/bin/env python3
"""Check the v0.2 fixed-cutoff theorem packet."""

from __future__ import annotations

from fractions import Fraction
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "src"))

PACKET = ROOT / "paper/fixed_cutoff_foundation_v0_2_0.md"
MATH_SPEC = ROOT / "docs/MATH_SPEC.md"
CLAIM_BOUNDARY = ROOT / "docs/CLAIM_BOUNDARY.md"
MODEL_DIFFERENCE = ROOT / "docs/APP_MODEL_DIFFERENCE.md"

from experiments._workflow.build_v0_2_support import build_crt_average_rows
from prime_clock_dynamics.multiplicity import (
    cutoff_multiplicity,
    multiplicity_covariance_baseline,
    multiplicity_moment_baseline,
)


def require(condition: bool, message: str, failures: list[str]) -> None:
    """Append ``message`` when ``condition`` is false."""
    if not condition:
        failures.append(message)


def require_phrases(path: Path, phrases: list[str], failures: list[str]) -> None:
    """Check that ``path`` contains all required phrases."""
    text = path.read_text(encoding="utf-8")
    for phrase in phrases:
        require(phrase in text, f"{path.relative_to(ROOT)} missing phrase: {phrase}", failures)


def product(values: list[int]) -> int:
    """Return product of integers."""
    result = 1
    for value in values:
        result *= value
    return result


def check_required_files(failures: list[str]) -> None:
    """Check packet and boundary files exist."""
    for path in [PACKET, MATH_SPEC, CLAIM_BOUNDARY, MODEL_DIFFERENCE]:
        require(path.is_file(), f"missing required file: {path.relative_to(ROOT)}", failures)


def check_packet_boundary(failures: list[str]) -> None:
    """Check theorem packet content and non-claim boundary."""
    require_phrases(
        PACKET,
        [
            "PrimeClock Dynamics v0.2.0 Fixed-Cutoff Foundation",
            "public v0.2.0 fixed-cutoff foundation artifact",
            "preprint",
            "not a DOI artifact",
            "not a Zenodo",
            "All fixed-cutoff statements below assume a finite set of distinct primes",
            "PCD-FC-0: Twelve-O'clock Fiber",
            "D(n, 0) = omega(n)",
            "PCD-FC-1: Fixed-Angle Residue Selector",
            "PCD-FC-2: Fixed-Cutoff CRT Mean And Variance",
            "PCD-FC-3: Fixed-Cutoff Two-Angle Covariance",
            "PCD-MG-1: Fixed-Cutoff CRT Average Identity",
            "sum_{0 <= n < M_x} U_x(n)",
            "prod_{p <= x}(1 - 1/p)",
            "PCD-MG-2: Finite-Window Periodic Discrepancy Bound",
            "Non-Claims",
            "Erdos-Kac CLT",
            "Gaussian field theorem",
            "diagonal theorem",
            "Mertens asymptotic law",
            "v0.3 diagonal bridge and v0.4 random-control diagnostics remain future",
        ],
        failures,
    )


def check_direction_boundary(failures: list[str]) -> None:
    """Check the packet is aligned with direction lock and app boundary."""
    require_phrases(
        MATH_SPEC,
        [
            "Residue-Time And Diagonal-Time Arcs",
            "diagonal app-level model",
            "D_x(n, alpha)",
            "D(n, alpha)",
        ],
        failures,
    )
    require_phrases(
        CLAIM_BOUNDARY,
        [
            "does not claim",
            "Erdos-Kac theorem",
            "Mertens' theorem",
            "peer-reviewed mathematical result",
        ],
        failures,
    )
    require_phrases(
        MODEL_DIFFERENCE,
        [
            "display surface, not the exact mathematical model",
            "visual arc strokes do not define `D(n, alpha)` or `U(n)`",
        ],
        failures,
    )


def check_crt_average_runner_spot(failures: list[str]) -> None:
    """Check the CRT average runner uses the fixed-cutoff residue period."""
    rows = build_crt_average_rows([5, 7])
    require(len(rows) == 2, "CRT average runner returned unexpected row count", failures)
    for row in rows:
        require(
            bool(row["exact_average_equals_product"]),
            "CRT average runner exact equality failed",
            failures,
        )
        require(row["average_minus_baseline_fraction"] == "0/1", "CRT exact diff nonzero", failures)
        require(int(row["sample_count"]) == int(row["crt_period"]), "sample count mismatch", failures)


def check_angular_moment_spot(failures: list[str]) -> None:
    """Check fixed-cutoff mean, variance, and covariance spots."""
    primes = [2, 3, 5, 7]
    period = product(primes)
    expected_mean, expected_variance = multiplicity_moment_baseline(primes)
    for alpha in [Fraction(0), Fraction(1, 10), Fraction(1, 3)]:
        values = [Fraction(cutoff_multiplicity(n, alpha, primes)) for n in range(period)]
        mean = sum(values, Fraction(0)) / period
        variance = sum((value - mean) ** 2 for value in values) / period
        require(mean == expected_mean, "fixed-cutoff mean mismatch", failures)
        require(variance == expected_variance, "fixed-cutoff variance mismatch", failures)

    for alpha, beta in [(Fraction(0), Fraction(1, 10)), (Fraction(1, 10), Fraction(1, 3))]:
        left_values = [Fraction(cutoff_multiplicity(n, alpha, primes)) for n in range(period)]
        right_values = [Fraction(cutoff_multiplicity(n, beta, primes)) for n in range(period)]
        left_mean = sum(left_values, Fraction(0)) / period
        right_mean = sum(right_values, Fraction(0)) / period
        covariance = (
            sum(
                (left - left_mean) * (right - right_mean)
                for left, right in zip(left_values, right_values)
            )
            / period
        )
        require(
            covariance == multiplicity_covariance_baseline(alpha, beta, primes),
            "fixed-cutoff covariance mismatch",
            failures,
        )


def main() -> None:
    failures: list[str] = []
    checks = [
        check_required_files,
        check_packet_boundary,
        check_direction_boundary,
        check_crt_average_runner_spot,
        check_angular_moment_spot,
    ]
    for check in checks:
        check(failures)

    if failures:
        print("check_fixed_cutoff_theorem_packet: failed")
        for failure in failures:
            print(f"FAIL: {failure}")
        raise SystemExit(1)
    print(f"check_fixed_cutoff_theorem_packet: checks={len(checks)}, failed=0")


if __name__ == "__main__":
    main()
