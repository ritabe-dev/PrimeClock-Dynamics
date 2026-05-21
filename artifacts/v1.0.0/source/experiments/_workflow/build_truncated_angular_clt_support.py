#!/usr/bin/env python3
"""Build deterministic support rows for the v0.6 truncated Angular CLT draft."""

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
from prime_clock_dynamics.multiplicity import multiplicity_moment_baseline
from prime_clock_dynamics.primes import primes_up_to


ARTIFACT_ID = "primeclock_dynamics_v0_6_truncated_angular_clt"
DEFAULT_CASES = [
    (10_000, 10, 2),
    (10_000_000, 31, 3),
    (100_000_000_000, 101, 4),
]


def fraction_text(value: Fraction) -> str:
    """Return stable numerator/denominator text."""
    return f"{value.numerator}/{value.denominator}"


def build_rows(cases: list[tuple[int, int, int]] | None = None) -> list[dict[str, object]]:
    """Return proof-budget rows for selected ``(N, y, m)`` cases."""
    rows: list[dict[str, object]] = []
    for window_size, cutoff, moment_order in cases or DEFAULT_CASES:
        prime_values = primes_up_to(cutoff)
        mean, variance = multiplicity_moment_baseline(prime_values)
        y_power = cutoff**moment_order
        pi_power = len(prime_values) ** moment_order
        variance_float = float(variance)
        normalized_pi_budget = pi_power / (window_size * (variance_float ** (moment_order / 2)))
        rows.append(
            {
                "window_size": window_size,
                "cutoff": cutoff,
                "moment_order": moment_order,
                "prime_count": len(prime_values),
                "mean_fraction": fraction_text(mean),
                "variance_fraction": fraction_text(variance),
                "variance": variance_float,
                "cutoff_power_over_window": y_power / window_size,
                "prime_count_power_over_window": pi_power / window_size,
                "prime_count_power_over_window_variance_scale": normalized_pi_budget,
                "satisfies_y_power_budget": y_power < window_size,
                "satisfies_prime_count_budget": pi_power < window_size,
                "satisfies_normalized_prime_count_budget": normalized_pi_budget < 1.0,
            }
        )
    return rows


def build_support(out_dir: Path, cases: list[tuple[int, int, int]] | None = None) -> dict[str, object]:
    """Write v0.6 support files and return the manifest."""
    out_dir.mkdir(parents=True, exist_ok=True)
    rows = build_rows(cases=cases)
    write_csv(out_dir / "truncated_angular_clt_support.csv", rows)
    manifest = {
        "artifact_id": ARTIFACT_ID,
        "support_status": "deterministic_v0_6_truncated_angular_clt_support",
        "files": [
            "truncated_angular_clt_support.csv",
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
            "note": "v0.6 truncated Angular CLT support evidence is deterministic proof-budget data.",
        },
    )
    return manifest


def parse_cases(value: str) -> list[tuple[int, int, int]]:
    """Parse comma-separated ``N:y:m`` cases."""
    cases: list[tuple[int, int, int]] = []
    for part in value.split(","):
        part = part.strip()
        if not part:
            continue
        pieces = part.split(":")
        if len(pieces) != 3:
            raise argparse.ArgumentTypeError("cases must use N:y:m entries")
        window_size, cutoff, moment_order = (int(piece) for piece in pieces)
        if window_size <= 0 or cutoff < 2 or moment_order <= 0:
            raise argparse.ArgumentTypeError("cases require N>0, y>=2, and m>0")
        cases.append((window_size, cutoff, moment_order))
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
        "build_truncated_angular_clt_support: "
        f"files={len(manifest['files'])}, rows={manifest['row_count']}",
    )


if __name__ == "__main__":
    main()
