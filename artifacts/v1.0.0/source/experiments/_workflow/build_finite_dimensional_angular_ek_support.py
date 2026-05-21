#!/usr/bin/env python3
"""Build deterministic support rows for the v0.9 finite-dimensional draft."""

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


ARTIFACT_ID = "primeclock_dynamics_v0_9_finite_dimensional_angular_ek"
DEFAULT_WINDOW_START = 10**12
DEFAULT_ANGLES = [
    ("zero", 0.0),
    ("one_tenth", 0.1),
    ("sqrt2_mod1", math.sqrt(2.0) % 1.0),
]


def stable_float(value: float) -> str:
    """Return stable compact text for proof-budget floats."""
    return format(value, ".12g")


def circular_distance(alpha: float, beta: float) -> float:
    """Return distance on R/Z for decimal support rows."""
    diff = abs(alpha - beta) % 1.0
    return min(diff, 1.0 - diff)


def slow_cutoff(window_start: int) -> int:
    """Return floor(N^(1/log log N)) for sufficiently large ``N``."""
    log_n = math.log(window_start)
    loglog_n = math.log(log_n)
    return max(2, int(math.floor(math.exp(log_n / loglog_n))))


def build_rows(
    window_start: int = DEFAULT_WINDOW_START,
    angles: list[tuple[str, float]] | None = None,
) -> list[dict[str, object]]:
    """Return pairwise finite-angle proof-budget rows."""
    angle_values = angles or DEFAULT_ANGLES
    cutoff = slow_cutoff(window_start)
    rows: list[dict[str, object]] = []
    for left_index, (left_label, left_alpha) in enumerate(angle_values):
        for right_label, right_alpha in angle_values[left_index + 1 :]:
            distance = circular_distance(left_alpha, right_alpha)
            collision_bound = math.ceil(1.0 / distance) if distance > 0 else math.inf
            rows.append(
                {
                    "window_start_N": window_start,
                    "window_end_2N": 2 * window_start,
                    "slow_cutoff_y": cutoff,
                    "angle_a": left_label,
                    "angle_b": right_label,
                    "alpha_a": stable_float(left_alpha),
                    "alpha_b": stable_float(right_alpha),
                    "circular_distance": stable_float(distance),
                    "same_residue_prime_safe_bound": collision_bound,
                    "same_residue_primes_finite": distance > 0,
                    "off_diagonal_covariance_status": "bounded_before_normalization",
                    "normalized_covariance_target": "off_diagonal_covariance/B_y^2 -> 0",
                    "cramer_wold_status": "gate_c_verified",
                    "tail_transfer_status": "v0.7 L1 tail removal applies anglewise",
                }
            )
    return rows


def build_support(out_dir: Path) -> dict[str, object]:
    """Write v0.9 support files and return the manifest."""
    out_dir.mkdir(parents=True, exist_ok=True)
    rows = build_rows()
    write_csv(out_dir / "finite_dimensional_angular_ek_support.csv", rows)
    manifest = {
        "artifact_id": ARTIFACT_ID,
        "support_status": "deterministic_v0_9_finite_dimensional_gate_c_support",
        "files": [
            "finite_dimensional_angular_ek_support.csv",
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
            "note": "v0.9 rows are deterministic proof-budget sanity checks, not statistical evidence.",
        },
    )
    return manifest


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out-dir", type=Path, required=True)
    args = parser.parse_args()
    manifest = build_support(args.out_dir)
    print(
        "build_finite_dimensional_angular_ek_support: "
        f"files={len(manifest['files'])}, rows={manifest['row_count']}",
    )


if __name__ == "__main__":
    main()
