#!/usr/bin/env python3
"""Generate v3.0 Mertens-boundary shared support experiments."""

from __future__ import annotations

import argparse
import csv
from fractions import Fraction
import hashlib
import json
import math
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "src"))

from prime_clock_dynamics.akc import normalizer_z
from prime_clock_dynamics.mertens_boundary import (
    cell_polynomial_coefficients,
    hard_q_point_factor,
    hard_two_point_local_factor,
    hard_weight,
    mertens_product,
    two_point_factor_type,
)
from prime_clock_dynamics.multiplicity import cutoff_multiplicity, selected_residue
from prime_clock_dynamics.primes import primes_up_to


EXPERIMENTS = [
    "01_one_prime_hard_normalizer",
    "02_q_point_hard_local_factor_exactness",
    "03_exact_cell_polynomial",
    "04_mertens_normalized_total_mass",
    "05_two_point_l2_route_support",
    "06_negative_beta_endpoint_diagnostic",
    "07_slow_integer_time_transfer_diagnostic",
]


def _format_float(value: float) -> str:
    value = round(float(value), 12)
    if abs(value) < 5e-15:
        value = 0.0
    return f"{value:.12e}"


def _format_fraction(value: Fraction) -> str:
    return f"{value.numerator}/{value.denominator}"


def _stable_value(value: object) -> object:
    if isinstance(value, float):
        return _format_float(value)
    if isinstance(value, Fraction):
        return _format_fraction(value)
    return value


def _write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    if not rows:
        raise ValueError(f"no rows for {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows({key: _stable_value(value) for key, value in row.items()} for row in rows)


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _residue_dict(n: int, primes: list[int]) -> dict[int, int]:
    return {p: n % p for p in primes}


def _direct_hard_q_point_average(primes: list[int], angles: list[Fraction]) -> Fraction:
    period = math.prod(primes)
    product = mertens_product(primes)
    total = Fraction(0)
    for n in range(period):
        value = Fraction(1, 1)
        for alpha in angles:
            if cutoff_multiplicity(n, alpha, primes) != 0:
                value = Fraction(0)
                break
            value *= Fraction(1, 1) / product
        total += value
    return total / period


def experiment_01_one_prime_hard_normalizer() -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for p in [2, 3, 5, 7, 11]:
        for alpha in [Fraction(0), Fraction(1, 7), Fraction(3, 10)]:
            selected = selected_residue(alpha, p)
            expectation = sum(hard_weight(residue == selected, p) for residue in range(p)) / p
            rows.append(
                {
                    "experiment_id": 1,
                    "prime": p,
                    "alpha": alpha,
                    "selected_residue": selected,
                    "one_prime_expectation": expectation,
                    "exact_equals_one": int(expectation == 1),
                    "status": "shared_hard_one_prime_normalizer_exact",
                }
            )
    return rows


def experiment_02_q_point_hard_local_factor_exactness() -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    cases = [
        (primes_up_to(5), [Fraction(0), Fraction(1, 9)]),
        (primes_up_to(5), [Fraction(0), Fraction(1, 9), Fraction(2, 9)]),
        (primes_up_to(7), [Fraction(1, 16), Fraction(3, 16), Fraction(5, 16)]),
    ]
    for case_id, (primes, angles) in enumerate(cases, start=1):
        direct = _direct_hard_q_point_average(primes, angles)
        formula = hard_q_point_factor(primes, angles)
        rows.append(
            {
                "experiment_id": 2,
                "case_id": case_id,
                "cutoff": max(primes),
                "q": len(angles),
                "direct_crt_average": direct,
                "hard_q_point_formula": formula,
                "exact_difference": direct - formula,
                "exact_match": int(direct == formula),
                "status": "shared_hard_q_point_formula_exact_enumeration",
            }
        )
    return rows


def experiment_03_exact_cell_polynomial() -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for seed in [0, 5, 17]:
        primes = primes_up_to(7)
        residues = _residue_dict(seed, primes)
        coefficients = cell_polynomial_coefficients(residues, primes)
        uncovered = coefficients.get(0, Fraction(0))
        normalized = uncovered / mertens_product(primes)
        for degree, coefficient in coefficients.items():
            rows.append(
                {
                    "experiment_id": 3,
                    "seed": seed,
                    "cutoff": max(primes),
                    "degree": degree,
                    "coefficient": coefficient,
                    "uncovered_coefficient": uncovered,
                    "mertens_normalized_uncovered": normalized,
                    "coefficient_sum_check": sum(coefficients.values()),
                    "status": "shared_cell_polynomial_exact_endpoint",
                }
            )
    return rows


def experiment_04_mertens_normalized_total_mass() -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for cutoff in [5, 7]:
        primes = primes_up_to(cutoff)
        period = math.prod(primes)
        values: list[Fraction] = []
        for n in range(period):
            coefficients = cell_polynomial_coefficients(_residue_dict(n, primes), primes)
            values.append(coefficients.get(0, Fraction(0)) / mertens_product(primes))
        mean = sum(values, Fraction(0)) / len(values)
        second_moment = sum(value * value for value in values) / len(values)
        rows.append(
            {
                "experiment_id": 4,
                "cutoff": cutoff,
                "period": period,
                "mean_normalized_total_mass": mean,
                "l2_total_mass": second_moment,
                "mean_exact_equals_one": int(mean == 1),
                "status": "shared_mertens_normalized_total_mass_exact",
            }
        )
    return rows


def experiment_05_two_point_l2_route_support() -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for cutoff in [31, 101, 251]:
        primes = primes_up_to(cutoff)
        for delta in [Fraction(1, 4), Fraction(1, 16), Fraction(1, 64), Fraction(1, 256)]:
            factors = [hard_two_point_local_factor(p, Fraction(0), delta) for p in primes]
            pair_factor = math.prod(float(factor) for factor in factors)
            collision_sum = sum(
                Fraction(1, p) for p in primes if two_point_factor_type(p, Fraction(0), delta) == "collision"
            )
            log_power_proxy = (1.0 + math.log(1.0 / float(delta))) ** 2
            rows.append(
                {
                    "experiment_id": 5,
                    "cutoff": cutoff,
                    "delta": delta,
                    "hard_two_point_factor": pair_factor,
                    "collision_reciprocal_sum": collision_sum,
                    "log_power_proxy": log_power_proxy,
                    "shell_integral_proxy": float(delta) * pair_factor,
                    "status": "shared_two_point_l2_route_diagnostic",
                }
            )
    return rows


def _mu_total_from_cell_polynomial(coefficients: dict[int, Fraction], primes: list[int], beta: float) -> float:
    u = math.exp(beta)
    numerator = sum(float(coefficient) * (u**degree) for degree, coefficient in coefficients.items())
    return numerator / normalizer_z(primes, beta)


def experiment_06_negative_beta_endpoint_diagnostic() -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    primes = primes_up_to(7)
    for seed in [0, 5, 17]:
        residues = _residue_dict(seed, primes)
        coefficients = cell_polynomial_coefficients(residues, primes)
        normalized_uncovered = float(coefficients.get(0, Fraction(0)) / mertens_product(primes))
        for beta in [-2.0, -4.0, -8.0, -12.0]:
            total = _mu_total_from_cell_polynomial(coefficients, primes, beta)
            rows.append(
                {
                    "experiment_id": 6,
                    "seed": seed,
                    "cutoff": max(primes),
                    "beta": beta,
                    "finite_beta_total_mass_exact_polynomial": total,
                    "mertens_normalized_uncovered": normalized_uncovered,
                    "abs_gap_to_mertens_normalized_uncovered": abs(total - normalized_uncovered),
                    "status": "shared_negative_beta_to_mertens_normalized_endpoint_exact_polynomial",
                }
            )
    return rows


def experiment_07_slow_integer_time_transfer_diagnostic() -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    primes = primes_up_to(5)
    period = math.prod(primes)
    crt_values = []
    for n in range(period):
        coefficients = cell_polynomial_coefficients(_residue_dict(n, primes), primes)
        crt_values.append(float(coefficients.get(0, Fraction(0)) / mertens_product(primes)))
    crt_mean = sum(crt_values) / len(crt_values)
    for multiplier in [2, 5, 11]:
        sample_size = multiplier * period + 3
        integer_values = []
        for n in range(1, sample_size + 1):
            coefficients = cell_polynomial_coefficients(_residue_dict(n, primes), primes)
            integer_values.append(float(coefficients.get(0, Fraction(0)) / mertens_product(primes)))
        integer_mean = sum(integer_values) / len(integer_values)
        rows.append(
            {
                "experiment_id": 7,
                "cutoff": max(primes),
                "crt_period": period,
                "sample_size": sample_size,
                "crt_mean": crt_mean,
                "integer_prefix_mean": integer_mean,
                "abs_gap": abs(integer_mean - crt_mean),
                "status": "diagnostic_only_slow_integer_time_transfer_seed_not_claim",
            }
        )
    return rows


def build_support(out_dir: Path) -> dict[str, object]:
    builders = [
        experiment_01_one_prime_hard_normalizer,
        experiment_02_q_point_hard_local_factor_exactness,
        experiment_03_exact_cell_polynomial,
        experiment_04_mertens_normalized_total_mass,
        experiment_05_two_point_l2_route_support,
        experiment_06_negative_beta_endpoint_diagnostic,
        experiment_07_slow_integer_time_transfer_diagnostic,
    ]
    out_dir.mkdir(parents=True, exist_ok=True)
    files: list[Path] = []
    summary: dict[str, object] = {
        "profile": "v3_0_mertens_boundary_shared_support",
        "experiment_count": len(builders),
        "experiments": [],
        "shared_review_support": True,
        "gate_c_claimed": False,
        "public_release_claimed": False,
        "integer_time_transfer_claimed": False,
        "diagonal_mertens_claimed": False,
        "high_point_theorem_claimed": False,
    }
    for index, builder in enumerate(builders, start=1):
        rows = builder()
        name = EXPERIMENTS[index - 1]
        path = out_dir / f"experiment_{index:02d}_{name}.csv"
        _write_csv(path, rows)
        files.append(path)
        summary["experiments"].append(
            {
                "id": index,
                "name": name,
                "file": path.name,
                "row_count": len(rows),
            }
        )
    summary_path = out_dir / "summary.json"
    summary_path.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    files.append(summary_path)
    sha_path = out_dir / "sha256.txt"
    sha_path.write_text("\n".join(f"{_sha256(path)}  {path.name}" for path in sorted(files)) + "\n", encoding="utf-8")
    return summary


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out-dir", type=Path, required=True)
    args = parser.parse_args()
    summary = build_support(args.out_dir)
    row_count = sum(int(item["row_count"]) for item in summary["experiments"])
    print(f"mb_v3_0_shared_support: experiments={summary['experiment_count']}, rows={row_count}")


if __name__ == "__main__":
    main()
