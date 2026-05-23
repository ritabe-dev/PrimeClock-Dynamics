#!/usr/bin/env python3
"""Generate focused v2.0 AKC public artifact support data."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "src"))

from experiments.akc.run_akc_v2_0_support_experiments import (
    _sha256,
    _write_csv,
    experiment_01_martingale_interval_check,
    experiment_02_q_point_moment_formula,
    experiment_03_l2_total_mass_stability,
    experiment_04_two_point_kernel_integrability,
    experiment_05_weak_convergence_diagnostics,
    experiment_06_gaussian_tangent_recovery,
)


EXPERIMENTS = [
    ("01_martingale_interval_check", experiment_01_martingale_interval_check),
    ("02_q_point_moment_formula", experiment_02_q_point_moment_formula),
    ("03_l2_total_mass_stability", experiment_03_l2_total_mass_stability),
    ("04_two_point_kernel_integrability", experiment_04_two_point_kernel_integrability),
    ("05_weak_convergence_diagnostics", experiment_05_weak_convergence_diagnostics),
    ("06_gaussian_tangent_recovery", experiment_06_gaussian_tangent_recovery),
]


PUBLIC_STATUS_BY_ID = {
    1: "public_martingale_identity_support",
    2: "public_q_point_formula_support",
    3: "public_l2_total_mass_support",
    4: "public_two_point_integrability_support",
    5: "public_weak_convergence_support",
    6: "public_gaussian_tangent_support",
}


def _public_rows(experiment_id: int, rows: list[dict[str, object]]) -> list[dict[str, object]]:
    status = PUBLIC_STATUS_BY_ID[experiment_id]
    return [{**row, "status": status} for row in rows]


def build_support(out_dir: Path) -> dict[str, object]:
    out_dir.mkdir(parents=True, exist_ok=True)
    files: list[Path] = []
    summary: dict[str, object] = {
        "profile": "v2_0_akc_public_support",
        "experiment_count": len(EXPERIMENTS),
        "experiments": [],
        "public_artifact_support": True,
        "public_release_claimed": True,
        "doi_claimed": False,
        "zenodo_claimed": False,
        "negative_beta_boundary_claimed": False,
        "high_point_theorem_claimed": False,
    }
    for index, (name, builder) in enumerate(EXPERIMENTS, start=1):
        rows = _public_rows(index, builder())
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
    summary = build_support(args.out_dir)
    row_count = sum(int(item["row_count"]) for item in summary["experiments"])
    print(f"akc_v2_0_public_support: experiments={summary['experiment_count']}, rows={row_count}")


if __name__ == "__main__":
    main()
