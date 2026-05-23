#!/usr/bin/env python3
"""Generate focused v3.0 Mertens-boundary public artifact support."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "src"))

from experiments.mb import run_mb_v3_0_support as shared_support


PUBLIC_BUILDERS = [
    shared_support.experiment_01_one_prime_hard_normalizer,
    shared_support.experiment_02_q_point_hard_local_factor_exactness,
    shared_support.experiment_03_exact_cell_polynomial,
    shared_support.experiment_04_mertens_normalized_total_mass,
    shared_support.experiment_05_two_point_l2_route_support,
    shared_support.experiment_06_negative_beta_endpoint_diagnostic,
]

PUBLIC_EXPERIMENTS = shared_support.EXPERIMENTS[:6]


def _public_rows(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    """Relabel shared support rows for the public artifact surface."""
    relabeled: list[dict[str, object]] = []
    for row in rows:
        item = dict(row)
        status = str(item.get("status", ""))
        if status.startswith("shared_"):
            item["status"] = "public_" + status[len("shared_") :]
        relabeled.append(item)
    return relabeled


def build_support(out_dir: Path) -> dict[str, object]:
    out_dir.mkdir(parents=True, exist_ok=True)
    files: list[Path] = []
    summary: dict[str, object] = {
        "profile": "v3_0_mertens_boundary_public_support",
        "experiment_count": len(PUBLIC_BUILDERS),
        "experiments": [],
        "public_artifact_support": True,
        "public_release_claimed": True,
        "doi_claimed": False,
        "zenodo_claimed": False,
        "integer_time_transfer_claimed": False,
        "diagonal_mertens_claimed": False,
        "high_point_theorem_claimed": False,
    }
    for index, builder in enumerate(PUBLIC_BUILDERS, start=1):
        rows = _public_rows(builder())
        name = PUBLIC_EXPERIMENTS[index - 1]
        path = out_dir / f"experiment_{index:02d}_{name}.csv"
        shared_support._write_csv(path, rows)
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
    sha_path.write_text(
        "\n".join(f"{shared_support._sha256(path)}  {path.name}" for path in sorted(files)) + "\n",
        encoding="utf-8",
    )
    return summary


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out-dir", type=Path, required=True)
    args = parser.parse_args()
    summary = build_support(args.out_dir)
    row_count = sum(int(item["row_count"]) for item in summary["experiments"])
    print(f"mb_v3_0_public_support: experiments={summary['experiment_count']}, rows={row_count}")


if __name__ == "__main__":
    main()
