#!/usr/bin/env python3
"""Check the v0.6 fixed-order finite-window moment bridge packet."""

from __future__ import annotations

from pathlib import Path
import tempfile
import sys


ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "src"))

PACKET = ROOT / "paper/truncated_angular_clt_v0_6.md"
SUPPORT_BUILDER = ROOT / "experiments/_workflow/build_truncated_angular_clt_support.py"

from experiments._workflow.build_truncated_angular_clt_support import build_rows, build_support


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
    """Check proof draft content and non-claim boundary."""
    require_phrases(
        PACKET,
        [
            "PrimeClock Dynamics v0.6 Fixed-Order Finite-Window Moment Bridge",
            "internal Gate C candidate proof packet",
            "not a public artifact",
            "not a preprint",
            "not a DOI artifact",
            "not a Zenodo record",
            "Truncated Finite-Window Model",
            "TFCLT-1: One Residue Class Per Prime",
            "TFCLT-2: Incomplete-Window CRT Counting Lemma",
            "TFCLT-3: Fixed-Order Factorial Moment Approximation",
            "TFCLT-4: Fixed-Order Centered Moment Comparison",
            "Z_p(n, alpha) = X_p(n, alpha) - 1/p",
            "O_m(pi(y)^m / N)",
            "pi(y)^m / (N B_y^m) -> 0",
            "TFCLT-5: Method-of-Moments Implication",
            "does not yet close this implication for a single fixed polynomial",
            "y^k / N -> 0",
            "y^m / N -> 0",
            "finite-window CLT theorem",
            "not the diagonal Angular Erdos-Kac theorem",
            "does not prove a diagonal Mertens uncovered law",
            "Gate R Support Evidence",
        ],
        failures,
    )


def check_support_rows(failures: list[str]) -> None:
    """Check deterministic support rows."""
    rows = build_rows()
    require(len(rows) == 3, "v0.6 support row count mismatch", failures)
    require([row["moment_order"] for row in rows] == [2, 3, 4], "moment orders mismatch", failures)
    require(all(float(row["variance"]) > 0 for row in rows), "variance must be positive", failures)
    require(
        all(row["satisfies_y_power_budget"] for row in rows),
        "all default rows should satisfy y^m < N",
        failures,
    )
    require(
        all(row["satisfies_prime_count_budget"] for row in rows),
        "all default rows should satisfy pi(y)^m < N",
        failures,
    )
    require(
        all(float(row["prime_count_power_over_window_variance_scale"]) >= 0 for row in rows),
        "normalized pi(y)^m/(N B_y^m) ratios must be nonnegative",
        failures,
    )
    require(
        all(row["satisfies_normalized_prime_count_budget"] for row in rows),
        "all default rows should satisfy normalized prime-count budget",
        failures,
    )
    require(
        rows[0]["cutoff_power_over_window"]
        > rows[1]["cutoff_power_over_window"]
        > rows[2]["cutoff_power_over_window"],
        "default y^m/N ratios should decrease",
        failures,
    )


def check_support_manifest(failures: list[str]) -> None:
    """Check support builder writes a manifest and expected files."""
    with tempfile.TemporaryDirectory(prefix="pcd_truncated_clt_support_") as tmp:
        manifest = build_support(Path(tmp))
        require(manifest["row_count"] == 3, "v0.6 support manifest row count mismatch", failures)
        require(
            manifest["artifact_id"] == "primeclock_dynamics_v0_6_truncated_angular_clt",
            "v0.6 support manifest artifact id mismatch",
            failures,
        )
        for filename in [
            "truncated_angular_clt_support.csv",
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
        print("check_truncated_angular_clt_packet: failed")
        for failure in failures:
            print(f"FAIL: {failure}")
        raise SystemExit(1)
    print(f"check_truncated_angular_clt_packet: checks={len(checks)}, failed=0")


if __name__ == "__main__":
    main()
