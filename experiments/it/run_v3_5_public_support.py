#!/usr/bin/env python3
"""Generate deterministic v3.5 public integer-time transfer support."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
from pathlib import Path
import sys
from typing import Callable

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

from prime_clock_dynamics.integer_time_transfer import (  # noqa: E402
    complete_period_average,
    complete_period_test_average,
    conductor_power_summary,
    dyadic_average,
    dyadic_residue_total_variation,
    dyadic_residue_total_variation_formula,
    dyadic_test_average,
    log_moment_budget_ratio,
    moment_transfer_bound,
    total_variation_expectation_bound,
    transfer_budget,
)


EXPERIMENT_ROWS = [
    {"N": 240, "cutoff_y": 5},
    {"N": 840, "cutoff_y": 7},
    {"N": 6000, "cutoff_y": 11},
]


def _format_float(value: float) -> str:
    value = float(value)
    if abs(value) < 5e-15:
        value = 0.0
    return f"{round(value, 12):.12e}"


def _stringify(value: object) -> str:
    if isinstance(value, float):
        return _format_float(value)
    return str(value)


def _summary_float(value: float) -> float:
    return float(_format_float(value))


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        for row in rows:
            writer.writerow({key: _stringify(value) for key, value in row.items()})


def experiment_total_variation_residue_audit() -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for spec in EXPERIMENT_ROWS:
        dyadic_n = int(spec["N"])
        cutoff_y = int(spec["cutoff_y"])
        budget = transfer_budget(cutoff_y, dyadic_n)
        tv = dyadic_residue_total_variation(dyadic_n, budget.primorial)
        quotient, remainder = divmod(dyadic_n, budget.primorial)
        exact_tv = dyadic_residue_total_variation_formula(dyadic_n, budget.primorial)
        bound = budget.primorial / dyadic_n
        rows.append(
            {
                "experiment": "total_variation_residue_audit",
                "N": dyadic_n,
                "cutoff_y": cutoff_y,
                "modulus_M_y": budget.primorial,
                "quotient_a": quotient,
                "remainder_b": remainder,
                "M_y_over_N": budget.primorial / dyadic_n,
                "total_variation_distance": tv,
                "tv_exact_formula_b_Q_minus_b_over_NQ": exact_tv,
                "absolute_gap_to_exact_formula": abs(tv - exact_tv),
                "tv_bound_M_y_over_N": bound,
                "within_tv_bound": tv <= bound,
                "status": "public_total_variation_residue_transfer_support",
            }
        )
    return rows


def _test_functions() -> list[tuple[str, Callable[[float], float], float]]:
    return [
        ("indicator_gt_one", lambda value: 1.0 if value > 1.0 else 0.0, 1.0),
        ("clipped_half_linear", lambda value: min(value, 2.0) / 2.0, 1.0),
        ("cosine_clipped", lambda value: math.cos(math.pi * min(value, 2.0) / 2.0), 1.0),
    ]


def experiment_bounded_test_transfer() -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for spec in EXPERIMENT_ROWS:
        dyadic_n = int(spec["N"])
        cutoff_y = int(spec["cutoff_y"])
        budget = transfer_budget(cutoff_y, dyadic_n)
        for name, test_fn, sup_norm in _test_functions():
            dyadic_value = dyadic_test_average(dyadic_n, cutoff_y, test_fn)
            period_value = complete_period_test_average(cutoff_y, test_fn)
            error = abs(dyadic_value - period_value)
            bound = total_variation_expectation_bound(
                budget.primorial,
                dyadic_n,
                sup_norm=sup_norm,
            )
            rows.append(
                {
                    "experiment": "bounded_test_function_transfer",
                    "N": dyadic_n,
                    "cutoff_y": cutoff_y,
                    "test_function": name,
                    "modulus_M_y": budget.primorial,
                    "dyadic_average": dyadic_value,
                    "complete_period_average": period_value,
                    "absolute_error_vs_period": error,
                    "tv_expectation_bound": bound,
                    "within_tv_expectation_bound": error <= bound,
                    "status": "public_bounded_test_distributional_transfer_support",
                }
            )
    return rows


def experiment_moment_transfer_sweep() -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for spec in EXPERIMENT_ROWS:
        dyadic_n = int(spec["N"])
        cutoff_y = int(spec["cutoff_y"])
        budget = transfer_budget(cutoff_y, dyadic_n)
        for moment in [1, 2, 3, 4]:
            dyadic_value = dyadic_average(dyadic_n, cutoff_y, power=moment)
            period_value = complete_period_average(cutoff_y, power=moment)
            error = abs(dyadic_value - period_value)
            bound = moment_transfer_bound(cutoff_y, dyadic_n, moment=moment)
            rows.append(
                {
                    "experiment": "moment_transfer_sweep",
                    "N": dyadic_n,
                    "cutoff_y": cutoff_y,
                    "moment": moment,
                    "modulus_M_y": budget.primorial,
                    "M_y_log_y_power_m_over_N": log_moment_budget_ratio(
                        cutoff_y,
                        dyadic_n,
                        moment=moment,
                    ),
                    "dyadic_moment": dyadic_value,
                    "complete_period_moment": period_value,
                    "absolute_error_vs_period": error,
                    "moment_transfer_bound": bound,
                    "within_moment_bound": error <= bound,
                    "status": "public_moment_transfer_support",
                }
            )
    return rows


def experiment_symbolic_cutoff_budget() -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    cases = [
        (10_000, "quarter_log", lambda value: max(2, int(0.25 * math.log(value)))),
        (100_000, "half_log", lambda value: max(2, int(0.50 * math.log(value)))),
        (1_000_000, "half_log", lambda value: max(2, int(0.50 * math.log(value)))),
        (
            1_000_000,
            "log_minus_2_loglog",
            lambda value: max(2, int(math.log(value) - 2.0 * math.log(math.log(value)))),
        ),
    ]
    for dyadic_n, rule_name, rule in cases:
        cutoff_y = rule(dyadic_n)
        budget = transfer_budget(cutoff_y, dyadic_n)
        row: dict[str, object] = {
            "experiment": "symbolic_cutoff_budget",
            "N": dyadic_n,
            "cutoff_rule": rule_name,
            "cutoff_y": cutoff_y,
            "modulus_M_y": budget.primorial,
            "M_y_over_N": budget.primorial / dyadic_n,
            "status": "public_symbolic_cutoff_budget_support",
        }
        for moment in [1, 2, 4]:
            row[f"M_y_log_y_power_{moment}_over_N"] = budget.log_moment_ratio(moment)
        rows.append(row)
    return rows


def experiment_conductor_projection_extension() -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for cutoff_y, low_bound, dyadic_n in [(5, 6, 240), (7, 10, 840), (7, 30, 840)]:
        summary = conductor_power_summary(cutoff_y, low_conductor_bound=low_bound)
        low_ratio = float(summary["low_conductor_power_ratio"])
        dyadic_mean = dyadic_average(dyadic_n, cutoff_y, power=1)
        rows.append(
            {
                "experiment": "conductor_projection_diagnostic",
                "N": dyadic_n,
                "cutoff_y": cutoff_y,
                "period": summary["period"],
                "low_conductor_bound": low_bound,
                "complete_period_mean": summary["mean"],
                "dyadic_mean": dyadic_mean,
                "total_centered_power": summary["total_centered_power"],
                "low_conductor_power": summary["low_conductor_power"],
                "high_conductor_power": summary["high_conductor_power"],
                "low_conductor_power_ratio": low_ratio,
                "high_conductor_power_ratio": 1.0 - low_ratio,
                "status": "public_conductor_projection_diagnostic_only",
            }
        )
    return rows


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def write_outputs(out_dir: Path) -> dict[str, object]:
    out_dir.mkdir(parents=True, exist_ok=True)
    tv_rows = experiment_total_variation_residue_audit()
    test_rows = experiment_bounded_test_transfer()
    moment_rows = experiment_moment_transfer_sweep()
    budget_rows = experiment_symbolic_cutoff_budget()
    conductor_rows = experiment_conductor_projection_extension()

    files = {
        "experiment_01_total_variation_residue_audit.csv": tv_rows,
        "experiment_02_bounded_test_function_transfer.csv": test_rows,
        "experiment_03_moment_transfer_sweep.csv": moment_rows,
        "experiment_04_symbolic_cutoff_budget.csv": budget_rows,
        "experiment_05_conductor_projection_diagnostics.csv": conductor_rows,
    }
    for name, rows in files.items():
        write_csv(out_dir / name, rows)

    summary = {
        "candidate_id": "pcd_v3_5_public_artifact",
        "artifact_status": "public_artifact",
        "public_artifact_support": True,
        "experiment_count": len(files),
        "row_count": sum(len(rows) for rows in files.values()),
        "public_release_claimed": True,
        "doi_claimed": False,
        "zenodo_claimed": False,
        "full_diagonal_claimed": False,
        "distributional_diagonal_claimed": False,
        "conductor_tail_theorem_claimed": False,
        "theorem_surface": ["PCD-IT-TV", "PCD-IT-DIST", "PCD-IT-MOM-m"],
        "all_tv_bounds_passed": all(row["within_tv_bound"] for row in tv_rows),
        "all_bounded_test_bounds_passed": all(
            row["within_tv_expectation_bound"] for row in test_rows
        ),
        "all_moment_bounds_passed": all(row["within_moment_bound"] for row in moment_rows),
        "max_tv_distance": _summary_float(
            max(float(row["total_variation_distance"]) for row in tv_rows)
        ),
        "max_bounded_test_error": _summary_float(
            max(float(row["absolute_error_vs_period"]) for row in test_rows)
        ),
        "max_moment_error": _summary_float(
            max(float(row["absolute_error_vs_period"]) for row in moment_rows)
        ),
        "min_low_conductor_power_ratio": _summary_float(
            min(float(row["low_conductor_power_ratio"]) for row in conductor_rows)
        ),
    }
    (out_dir / "summary.json").write_text(
        json.dumps(summary, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )

    digest_rows = []
    for path in sorted(out_dir.glob("*")):
        if path.name == "sha256.txt" or not path.is_file():
            continue
        digest_rows.append(f"{sha256_file(path)}  {path.name}")
    (out_dir / "sha256.txt").write_text("\n".join(digest_rows) + "\n", encoding="utf-8")
    return summary


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out-dir", type=Path, required=True)
    args = parser.parse_args()
    summary = write_outputs(args.out_dir)
    print(
        "it_v3_5_public_support: "
        f"experiments={summary['experiment_count']} rows={summary['row_count']} "
        f"out={args.out_dir}"
    )


if __name__ == "__main__":
    main()
