#!/usr/bin/env python3
"""Generate shared v2.0 AKC support experiments.

These builders support the complete-CRT finite-beta AKC measure route and are
reused by focused support wrappers. Boundary diagnostics remain outside the
current theorem surface.
"""

from __future__ import annotations

import argparse
import csv
from fractions import Fraction
import hashlib
import json
import math
from pathlib import Path
import sys
from typing import Callable

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "src"))

from prime_clock_dynamics.akc import normalizer_z, q_point_moment_factor
from prime_clock_dynamics.collision_kernel import collision_kernel
from prime_clock_dynamics.multiplicity import cutoff_multiplicity, selected_residue
from prime_clock_dynamics.primes import primes_up_to


EXPERIMENTS = [
    "01_martingale_interval_check",
    "02_q_point_moment_formula",
    "03_l2_total_mass_stability",
    "04_two_point_kernel_integrability",
    "05_weak_convergence_diagnostics",
    "06_gaussian_tangent_recovery",
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


def _density_at_alpha(residues: dict[int, int], primes: list[int], beta: float, alpha: Fraction) -> float:
    hits = sum(1 for p in primes if residues[p] == selected_residue(alpha, p))
    return math.exp(beta * hits) / normalizer_z(primes, beta)


def _grid_integral(
    residues: dict[int, int],
    primes: list[int],
    beta: float,
    predicate: Callable[[Fraction], bool],
    *,
    grid_size: int = 84,
) -> float:
    total = 0.0
    for index in range(grid_size):
        alpha = Fraction(index, grid_size)
        if predicate(alpha):
            total += _density_at_alpha(residues, primes, beta, alpha)
    return total / grid_size


def _test_function_value(name: str, alpha: Fraction) -> float:
    x = float(alpha)
    if name == "one":
        return 1.0
    if name == "cos_1":
        return math.cos(2.0 * math.pi * x)
    if name == "sin_1":
        return math.sin(2.0 * math.pi * x)
    if name == "interval_0_1_2":
        return 1.0 if Fraction(0) <= alpha < Fraction(1, 2) else 0.0
    raise ValueError(f"unknown test function: {name}")


def _grid_test_integral(
    residues: dict[int, int],
    primes: list[int],
    beta: float,
    test_function: str,
    *,
    grid_size: int = 84,
) -> float:
    total = 0.0
    for index in range(grid_size):
        alpha = Fraction(index, grid_size)
        total += _test_function_value(test_function, alpha) * _density_at_alpha(residues, primes, beta, alpha)
    return total / grid_size


def experiment_01_martingale_interval_check() -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    base_primes = [2, 3, 5]
    intervals = [
        ("[0,1/2)", Fraction(0), Fraction(1, 2)),
        ("[1/3,2/3)", Fraction(1, 3), Fraction(2, 3)),
    ]
    for beta in [-1.0, 0.5, 1.0]:
        for new_prime in [7, 11]:
            for n in [0, 17, 29]:
                base_residues = _residue_dict(n, base_primes)
                for label, left, right in intervals:
                    old_mass = _grid_integral(
                        base_residues,
                        base_primes,
                        beta,
                        lambda alpha, left=left, right=right: left <= alpha < right,
                    )
                    conditional = 0.0
                    for new_residue in range(new_prime):
                        residues = dict(base_residues)
                        residues[new_prime] = new_residue
                        conditional += _grid_integral(
                            residues,
                            [*base_primes, new_prime],
                            beta,
                            lambda alpha, left=left, right=right: left <= alpha < right,
                        )
                    conditional /= new_prime
                    rows.append(
                        {
                            "experiment_id": 1,
                            "beta": beta,
                            "base_cutoff": max(base_primes),
                            "new_prime": new_prime,
                            "n_residue_seed": n,
                            "interval": label,
                            "old_mass": old_mass,
                            "conditional_next_mass": conditional,
                            "abs_error": abs(old_mass - conditional),
                            "status": "support_martingale_identity_grid_check",
                        }
                    )
    return rows


def _direct_q_point_average(primes: list[int], angles: list[Fraction], beta: float) -> float:
    period = math.prod(primes)
    total = 0.0
    normalizer = normalizer_z(primes, beta)
    for n in range(period):
        value = 1.0
        for alpha in angles:
            value *= math.exp(beta * cutoff_multiplicity(n, alpha, primes)) / normalizer
        total += value
    return total / period


def experiment_02_q_point_moment_formula() -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    cases = [
        (primes_up_to(7), [Fraction(0), Fraction(1, 9)], 0.75),
        (primes_up_to(7), [Fraction(0), Fraction(1, 9), Fraction(2, 9)], -0.5),
        (primes_up_to(11), [Fraction(1, 16), Fraction(3, 16), Fraction(5, 16)], 0.4),
    ]
    for case_id, (primes, angles, beta) in enumerate(cases, start=1):
        direct = _direct_q_point_average(primes, angles, beta)
        formula = q_point_moment_factor(primes, angles, beta)
        rows.append(
            {
                "experiment_id": 2,
                "case_id": case_id,
                "cutoff": max(primes),
                "q": len(angles),
                "beta": beta,
                "direct_crt_average": direct,
                "hcgf_q_point_formula": formula,
                "abs_error": abs(direct - formula),
                "status": "support_q_point_formula_exact_enumeration",
            }
        )
    return rows


def _all_mu_total_values(primes: list[int], beta: float) -> list[float]:
    period = math.prod(primes)
    return [_grid_integral(_residue_dict(n, primes), primes, beta, lambda _alpha: True) for n in range(period)]


def experiment_03_l2_total_mass_stability() -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for beta in [-1.0, 0.5, 1.0, 1.5]:
        previous_l2 = ""
        for cutoff in [5, 7]:
            primes = primes_up_to(cutoff)
            values = _all_mu_total_values(primes, beta)
            mean = sum(values) / len(values)
            l2_value = sum(value * value for value in values) / len(values)
            rows.append(
                {
                    "experiment_id": 3,
                    "beta": beta,
                    "cutoff": cutoff,
                    "period": math.prod(primes),
                    "mean_total_mass": mean,
                    "l2_total_mass": l2_value,
                    "previous_l2_total_mass": previous_l2,
                    "l2_growth_from_previous": "" if previous_l2 == "" else l2_value - float(previous_l2),
                    "status": "support_l2_total_mass_stability_diagnostic",
                }
            )
            previous_l2 = _format_float(l2_value)
    return rows


def experiment_04_two_point_kernel_integrability() -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    beta = 1.0
    exponent = (math.exp(beta) - 1.0) ** 2
    for cutoff in [31, 101, 251]:
        primes = primes_up_to(cutoff)
        for delta in [Fraction(1, 4), Fraction(1, 16), Fraction(1, 64), Fraction(1, 256)]:
            pair_factor = q_point_moment_factor(primes, [Fraction(0), delta], beta)
            log_power_proxy = (1.0 + math.log(1.0 / float(delta))) ** exponent
            shell_width = float(delta)
            rows.append(
                {
                    "experiment_id": 4,
                    "cutoff": cutoff,
                    "beta": beta,
                    "delta": _format_fraction(delta),
                    "two_point_moment_factor": pair_factor,
                    "log_power_proxy": log_power_proxy,
                    "shell_integral_proxy": shell_width * pair_factor,
                    "status": "support_two_point_integrability_diagnostic",
                }
            )
    return rows


def experiment_05_weak_convergence_diagnostics() -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    test_functions = ["one", "cos_1", "sin_1", "interval_0_1_2"]
    for beta in [-0.75, 0.75]:
        previous_by_function: dict[str, float] = {}
        for cutoff in [5, 7]:
            primes = primes_up_to(cutoff)
            period = math.prod(primes)
            for test_function in test_functions:
                values = [
                    _grid_test_integral(_residue_dict(n, primes), primes, beta, test_function)
                    for n in range(period)
                ]
                mean = sum(values) / len(values)
                variance = sum((value - mean) ** 2 for value in values) / len(values)
                previous = previous_by_function.get(test_function)
                rows.append(
                    {
                        "experiment_id": 5,
                        "beta": beta,
                        "cutoff": cutoff,
                        "test_function": test_function,
                        "mean": mean,
                        "variance": variance,
                        "delta_from_previous_cutoff": "" if previous is None else mean - previous,
                        "status": "support_weak_convergence_test_function_diagnostic",
                    }
                )
                previous_by_function[test_function] = mean
    return rows


def experiment_06_gaussian_tangent_recovery() -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    primes = primes_up_to(101)
    pairs = [(Fraction(0), Fraction(1, 31)), (Fraction(1, 17), Fraction(3, 17))]
    for case_id, (alpha, gamma) in enumerate(pairs, start=1):
        kernel = float(collision_kernel(primes, alpha, gamma))
        for beta in [0.01, 0.03, 0.05]:
            moment = q_point_moment_factor(primes, [alpha, gamma], beta)
            tangent_estimate = math.log(moment) / (beta * beta)
            rows.append(
                {
                    "experiment_id": 6,
                    "case_id": case_id,
                    "cutoff": max(primes),
                    "beta": beta,
                    "alpha": _format_fraction(alpha),
                    "gamma": _format_fraction(gamma),
                    "collision_kernel": kernel,
                    "log_moment_over_beta_squared": tangent_estimate,
                    "abs_error": abs(tangent_estimate - kernel),
                    "status": "support_gaussian_tangent_recovery_diagnostic",
                }
            )
    return rows


def build_experiments(out_dir: Path) -> dict[str, object]:
    builders = [
        experiment_01_martingale_interval_check,
        experiment_02_q_point_moment_formula,
        experiment_03_l2_total_mass_stability,
        experiment_04_two_point_kernel_integrability,
        experiment_05_weak_convergence_diagnostics,
        experiment_06_gaussian_tangent_recovery,
    ]
    out_dir.mkdir(parents=True, exist_ok=True)
    files: list[Path] = []
    summary: dict[str, object] = {
        "profile": "v2_0_akc_shared_support",
        "experiment_count": len(builders),
        "experiments": [],
        "future_release_claimed": False,
        "public_release_claimed": False,
        "integer_time_transfer_claimed": False,
        "diagonal_mertens_claimed": False,
        "negative_beta_boundary_claimed": False,
        "high_point_theorem_claimed": False,
        "lee_yang_theorem_claimed": False,
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
    sha_lines = [f"{_sha256(path)}  {path.name}" for path in sorted(files)]
    sha_path = out_dir / "sha256.txt"
    sha_path.write_text("\n".join(sha_lines) + "\n", encoding="utf-8")
    return summary


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out-dir", type=Path, required=True)
    args = parser.parse_args()
    summary = build_experiments(args.out_dir)
    row_count = sum(int(item["row_count"]) for item in summary["experiments"])
    print(f"akc_v2_0_support_experiments: experiments={summary['experiment_count']}, rows={row_count}")


if __name__ == "__main__":
    main()
