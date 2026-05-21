#!/usr/bin/env python3
"""Check the v0.7 all-angle L1 diagonal tail-removal packet."""

from __future__ import annotations

from pathlib import Path
import sys
import tempfile


ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "src"))

PACKET = ROOT / "paper/diagonal_tail_removal_v0_7.md"
SUPPORT_BUILDER = ROOT / "experiments/_workflow/build_diagonal_tail_support.py"

from experiments._workflow.build_diagonal_tail_support import build_rows, build_support


def require(condition: bool, message: str, failures: list[str]) -> None:
    """Append ``message`` when ``condition`` is false."""
    if not condition:
        failures.append(message)


def require_phrases(path: Path, phrases: list[str], failures: list[str]) -> None:
    """Check that ``path`` contains all required phrases."""
    text = path.read_text(encoding="utf-8")
    for phrase in phrases:
        require(phrase in text, f"{path.relative_to(ROOT)} missing phrase: {phrase}", failures)


def check_required_files(failures: list[str]) -> None:
    """Check packet and support builder exist."""
    for path in [PACKET, SUPPORT_BUILDER]:
        require(path.is_file(), f"missing required file: {path.relative_to(ROOT)}", failures)


def check_packet_boundary(failures: list[str]) -> None:
    """Check draft content and non-claim boundary."""
    require_phrases(
        PACKET,
        [
            "PrimeClock Dynamics v0.7 All-Angle L1 Diagonal Tail Removal",
            "internal Gate C candidate proof packet for all-angle L1 diagonal tail",
            "Gate C candidate for an all-angle L1 diagonal tail-removal",
            "not a diagonal Angular Erdos-Kac theorem",
            "not a public artifact",
            "DT-1: Dyadic Diagonal And Truncated Variables",
            "N < n <= 2N",
            "T_y(n, alpha) = D_n(n, alpha) - D_y(n, alpha)",
            "DT-2: Slow Truncation",
            "y(N) = floor(N^(1/log log N))",
            "y(N)^k / N = N^(k/log log N - 1) -> 0",
            "DT-3: Centering And Scale Comparisons",
            "(A_{2N} - A_y) / B_{2N} -> 0",
            "B_y / B_{2N} -> 1",
            "DT-4: All-Angle L1 Tail Bound",
            "E_{N < n <= 2N}[T_y(n, alpha)] = O(log log log N)",
            "Markov's inequality",
            "PCD-AK-DT-L1",
            "DT-5: Slutsky Bridge",
            "Slutsky's theorem",
            "DT-6: Optional Rational-Angle Pointwise Lemma",
            "PCD-AK-DT-RAT",
            "DT-7: Former Irrational Tail-Moment Route",
            "does not claim an arbitrary irrational-angle tail moment bound",
            "Gate C Support Evidence",
            "not statistical evidence and not a theorem",
        ],
        failures,
    )


def check_support_rows(failures: list[str]) -> None:
    """Check deterministic support rows."""
    rows = build_rows()
    require(len(rows) == 3, "v0.7 support row count mismatch", failures)
    require([row["moment_order"] for row in rows] == [2, 3, 4], "moment orders mismatch", failures)
    require(
        all(row["truncation"] == "floor(N^(1/loglogN))" for row in rows),
        "slow truncation label mismatch",
        failures,
    )
    require(all(row["theta_fraction"] == "1/loglogN" for row in rows), "theta label mismatch", failures)
    require(all(int(row["cutoff"]) >= 2 for row in rows), "cutoffs must be >= 2", failures)
    require(all(float(row["cutoff_variance"]) > 0 for row in rows), "cutoff variance must be positive", failures)
    require(all(float(row["dyadic_variance"]) > 0 for row in rows), "dyadic variance must be positive", failures)
    require(
        all(float(row["tail_prime_harmonic"]) >= 0 for row in rows),
        "tail harmonic baselines must be nonnegative",
        failures,
    )
    require(
        all(float(row["tail_mean_over_dyadic_scale"]) >= 0 for row in rows),
        "normalized tail mean baselines must be nonnegative",
        failures,
    )
    require(
        all(float(row["centering_gap_over_dyadic_scale"]) >= 0 for row in rows),
        "centering gap ratios must be nonnegative",
        failures,
    )
    require(
        all(0 < float(row["scale_ratio_B_y_over_B_2N"]) <= 1 for row in rows),
        "scale ratios must be in (0, 1]",
        failures,
    )
    require(
        all(isinstance(row["tail_prime_harmonic"], str) for row in rows),
        "float-like support values should be stable strings",
        failures,
    )
    require(
        all(row["v0_6_y_power_budget_asymptotic"] for row in rows),
        "all default rows should record v0.6 asymptotic budget",
        failures,
    )
    require(
        all(row["tail_l1_markov_target"] == "E[T_y]/B_2N -> 0" for row in rows),
        "all default rows should record L1 Markov target",
        failures,
    )
    require(
        all(row["uses_tail_moment_bound"] is False for row in rows),
        "L1 support rows should not use tail moment bounds",
        failures,
    )


def check_support_manifest(failures: list[str]) -> None:
    """Check support builder writes a manifest and expected files."""
    with tempfile.TemporaryDirectory(prefix="pcd_diagonal_tail_support_") as tmp:
        manifest = build_support(Path(tmp))
        require(manifest["row_count"] == 3, "v0.7 support manifest row count mismatch", failures)
        require(
            manifest["artifact_id"] == "primeclock_dynamics_v0_7_diagonal_tail_removal",
            "v0.7 support manifest artifact id mismatch",
            failures,
        )
        for filename in [
            "diagonal_tail_support.csv",
            "support_manifest.json",
            "support_metadata.json",
        ]:
            require((Path(tmp) / filename).is_file(), f"missing support output: {filename}", failures)


def main() -> None:
    failures: list[str] = []
    checks = [
        check_required_files,
        check_packet_boundary,
        check_support_rows,
        check_support_manifest,
    ]
    for check in checks:
        check(failures)

    if failures:
        print("check_diagonal_tail_removal_packet: failed")
        for failure in failures:
            print(f"FAIL: {failure}")
        raise SystemExit(1)
    print(f"check_diagonal_tail_removal_packet: checks={len(checks)}, failed=0")


if __name__ == "__main__":
    main()
