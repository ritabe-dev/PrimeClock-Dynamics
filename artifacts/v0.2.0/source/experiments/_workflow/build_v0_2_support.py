#!/usr/bin/env python3
"""Build deterministic support evidence for the v0.2.0 public artifact."""

from __future__ import annotations

import argparse
import json
from fractions import Fraction
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "src"))

from prime_clock_dynamics.experiments import write_csv, write_metadata
from prime_clock_dynamics.multiplicity import (
    cutoff_multiplicity,
    multiplicity_covariance_baseline,
    multiplicity_moment_baseline,
)
from prime_clock_dynamics.primes import omega, primes_up_to
from prime_clock_dynamics.uncovered import cutoff_uncovered_measure


ARTIFACT_ID = "primeclock_dynamics_v0_2_0_fixed_cutoff_foundation"
CUTOFFS = [5, 7, 11, 13]
PRIME_SET = [2, 3, 5, 7]
ANGLES = {
    "zero": Fraction(0),
    "one_tenth": Fraction(1, 10),
    "one_third": Fraction(1, 3),
}


def product(values: list[int]) -> int:
    """Return product of integers."""
    result = 1
    for value in values:
        result *= value
    return result


def fraction_text(value: Fraction) -> str:
    """Return stable numerator/denominator text."""
    return f"{value.numerator}/{value.denominator}"


def mertens_product_fraction(prime_values: list[int]) -> Fraction:
    """Return exact ``prod_p (1 - 1/p)`` for a fixed prime set."""
    baseline = Fraction(1)
    for prime in prime_values:
        baseline *= Fraction(prime - 1, prime)
    return baseline


def build_crt_average_rows(cutoffs: list[int]) -> list[dict[str, object]]:
    """Return exact fixed-cutoff CRT-average support rows."""
    rows: list[dict[str, object]] = []
    for cutoff in cutoffs:
        prime_values = primes_up_to(cutoff)
        period = product(prime_values)
        baseline_fraction = mertens_product_fraction(prime_values)
        baseline = float(baseline_fraction)
        measures = [cutoff_uncovered_measure(n, cutoff) for n in range(period)]
        average = sum(measures, Fraction(0)) / period
        exact_difference = average - baseline_fraction
        average_float = float(average)
        pointwise_differences = [abs(float(measure) - baseline) for measure in measures]
        rows.append(
            {
                "cutoff": cutoff,
                "primes": " ".join(str(prime) for prime in prime_values),
                "crt_period": period,
                "sample_count": period,
                "average_uncovered_measure": average_float,
                "average_uncovered_measure_fraction": fraction_text(average),
                "mertens_product_baseline": baseline,
                "mertens_product_baseline_fraction": fraction_text(baseline_fraction),
                "average_minus_baseline": average_float - baseline,
                "average_minus_baseline_fraction": fraction_text(exact_difference),
                "absolute_average_minus_baseline": abs(average_float - baseline),
                "exact_average_equals_product": average == baseline_fraction,
                "min_uncovered_measure": float(min(measures)),
                "max_uncovered_measure": float(max(measures)),
                "max_pointwise_abs_difference": max(pointwise_differences),
            }
        )
    return rows


def build_theorem0_summary() -> dict[str, object]:
    """Return support summary for ``D(n,0)=omega(n)`` through 10000."""
    prime_pool = primes_up_to(10000)
    checked = 0
    for n in range(2, 10001):
        actual = sum(1 for p in prime_pool if p <= n and n % p == 0)
        if actual != omega(n):
            raise RuntimeError(f"Theorem 0 support mismatch at n={n}")
        checked += 1
    return {
        "support": "theorem0",
        "range_start": 2,
        "range_end": 10000,
        "checked_values": checked,
        "all_match": True,
    }


def build_angular_moment_rows() -> list[dict[str, object]]:
    """Return exact CRT-period moment and covariance support rows."""
    period = product(PRIME_SET)
    expected_mean, expected_variance = multiplicity_moment_baseline(PRIME_SET)
    rows: list[dict[str, object]] = []

    for angle_name, alpha in ANGLES.items():
        values = [Fraction(cutoff_multiplicity(n, alpha, PRIME_SET)) for n in range(period)]
        mean = sum(values, Fraction(0)) / period
        variance = sum((value - mean) ** 2 for value in values) / period
        rows.append(
            {
                "support": "moment",
                "angle_a": angle_name,
                "angle_b": "",
                "alpha_a": fraction_text(alpha),
                "alpha_b": "",
                "prime_set": " ".join(str(prime) for prime in PRIME_SET),
                "crt_period": period,
                "mean_fraction": fraction_text(mean),
                "expected_mean_fraction": fraction_text(expected_mean),
                "variance_fraction": fraction_text(variance),
                "expected_variance_fraction": fraction_text(expected_variance),
                "covariance_fraction": "",
                "expected_covariance_fraction": "",
                "exact_match": mean == expected_mean and variance == expected_variance,
            }
        )

    angle_items = list(ANGLES.items())
    for index, (left_name, alpha) in enumerate(angle_items):
        for right_name, beta in angle_items[index:]:
            left_values = [Fraction(cutoff_multiplicity(n, alpha, PRIME_SET)) for n in range(period)]
            right_values = [Fraction(cutoff_multiplicity(n, beta, PRIME_SET)) for n in range(period)]
            left_mean = sum(left_values, Fraction(0)) / period
            right_mean = sum(right_values, Fraction(0)) / period
            covariance = (
                sum(
                    (left - left_mean) * (right - right_mean)
                    for left, right in zip(left_values, right_values)
                )
                / period
            )
            expected_covariance = multiplicity_covariance_baseline(alpha, beta, PRIME_SET)
            rows.append(
                {
                    "support": "covariance",
                    "angle_a": left_name,
                    "angle_b": right_name,
                    "alpha_a": fraction_text(alpha),
                    "alpha_b": fraction_text(beta),
                    "prime_set": " ".join(str(prime) for prime in PRIME_SET),
                    "crt_period": period,
                    "mean_fraction": fraction_text(left_mean),
                    "expected_mean_fraction": fraction_text(expected_mean),
                    "variance_fraction": "",
                    "expected_variance_fraction": "",
                    "covariance_fraction": fraction_text(covariance),
                    "expected_covariance_fraction": fraction_text(expected_covariance),
                    "exact_match": covariance == expected_covariance,
                }
            )
    return rows


def build_support(out_dir: Path) -> dict[str, object]:
    """Write deterministic support files and return the support manifest."""
    out_dir.mkdir(parents=True, exist_ok=True)

    crt_rows = build_crt_average_rows(CUTOFFS)
    write_csv(out_dir / "crt_average_support.csv", crt_rows)

    angular_rows = build_angular_moment_rows()
    write_csv(out_dir / "angular_moment_support.csv", angular_rows)

    theorem0_summary = build_theorem0_summary()
    (out_dir / "theorem0_support.json").write_text(
        json.dumps(theorem0_summary, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )

    manifest = {
        "artifact_id": ARTIFACT_ID,
        "support_status": "deterministic_v0_2_support",
        "cutoffs": CUTOFFS,
        "angular_prime_set": PRIME_SET,
        "angular_angles": {name: fraction_text(alpha) for name, alpha in ANGLES.items()},
        "files": [
            "crt_average_support.csv",
            "angular_moment_support.csv",
            "theorem0_support.json",
            "support_metadata.json",
        ],
        "crt_average_rows": len(crt_rows),
        "angular_support_rows": len(angular_rows),
        "theorem0_checked_values": theorem0_summary["checked_values"],
    }
    (out_dir / "support_manifest.json").write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    write_metadata(
        out_dir / "support_metadata.json",
        {
            "artifact_id": manifest["artifact_id"],
            "note": "v0.2.0 fixed-cutoff support evidence is deterministic.",
        },
    )
    return manifest


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out-dir", type=Path, required=True)
    args = parser.parse_args()
    manifest = build_support(args.out_dir)
    print(
        "build_v0_2_support: "
        f"files={len(manifest['files'])}, theorem0_checked={manifest['theorem0_checked_values']}",
    )


if __name__ == "__main__":
    main()
