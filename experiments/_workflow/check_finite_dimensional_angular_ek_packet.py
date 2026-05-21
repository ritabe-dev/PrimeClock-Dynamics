#!/usr/bin/env python3
"""Check the v0.9 finite-dimensional Angular Erdos-Kac Gate C verified record."""

from __future__ import annotations

import argparse
import csv
import json
import tempfile
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "src"))

from experiments._workflow.build_finite_dimensional_angular_ek_support import build_support


PACKET = ROOT / "paper/finite_dimensional_angular_ek_v0_9.md"
REVIEW_PACKET = ROOT / "experiments/_workflow/V0_9_GATE_R_REVIEW_PACKET.md"
PASS_RECORD = ROOT / "experiments/_workflow/V0_9_GATE_R_PASS_RECORD.md"
PROPOSITION_STATUS = ROOT / "experiments/_workflow/PROPOSITION_STATUS.md"
CLAIM_BOUNDARY = ROOT / "docs/CLAIM_BOUNDARY.md"
WORKFLOW = ROOT / "experiments/_workflow/pcd_v0_9_finite_dimensional_angular_ek_gate_r.json"


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
    """Check v0.9 draft files exist."""
    for path in [PACKET, REVIEW_PACKET, PASS_RECORD, PROPOSITION_STATUS, CLAIM_BOUNDARY, WORKFLOW]:
        require(path.is_file(), f"missing required file: {path.relative_to(ROOT)}", failures)


def check_workflow(failures: list[str]) -> None:
    """Check v0.9 workflow shape."""
    data = json.loads(WORKFLOW.read_text(encoding="utf-8"))
    require(
        data.get("candidate_id") == "pcd_v0_9_finite_dimensional_angular_ek_gate_r",
        "bad workflow id",
        failures,
    )
    require(data.get("status") == "gate_r_passed", "bad workflow status", failures)
    require(data.get("public_release") is False, "workflow must not be public", failures)
    gates = data.get("gates")
    require(isinstance(gates, dict) and "quick" in gates, "workflow missing quick gate", failures)


def check_packet(failures: list[str]) -> None:
    """Check v0.9 paper wording and boundaries."""
    require_phrases(
        PACKET,
        [
            "PrimeClock Dynamics v0.9 Finite-Dimensional Angular Erdos-Kac Gate C Verified",
            "fixed and pairwise distinct",
            "FDEK-1: Target Joint Statement",
            "Gate C verified statement",
            "independent standard normal random variables",
            "FDEK-2: Pairwise Residue-Collision Bound",
            "p < 1/delta",
            "p <= ceil(1/delta)",
            "FDEK-3: Complete-CRT Covariance Structure",
            "off-diagonal covariance tends to `0`",
            "FDEK-4: Cramer-Wold Reduction",
            "V_y(t) = (sum_{j=1}^d t_j^2) B_y^2 + O_{alpha,t}(1)",
            "sum_{j=1}^d t_j^2",
            "FDEK-5: Finite-Window Transfer at the Slow Cutoff",
            "two different residue classes modulo the same prime",
            "O_m(pi(y)^m/N)",
            "FDEK-6: Diagonal Tail and Slutsky",
            "union bound",
            "Gate C verified route",
            "PCD-AK-FD-JOINT",
            "does not claim",
            "shrinking-angle theorem",
        ],
        failures,
    )
    require_phrases(
        REVIEW_PACKET,
        [
            "v0.9 Gate R Review Packet",
            "finite-dimensional fixed-angle",
            "pairwise selected-residue collisions",
            "Cramer-Wold projections",
            "Gate R passed",
        ],
        failures,
    )
    require_phrases(
        PASS_RECORD,
        [
            "v0.9 Gate R Pass Record",
            "Gate R passed for `PCD-AK-FD-JOINT`",
            "p < 1/delta",
            "V_y(t) = (sum_j t_j^2) B_y^2 + O_{alpha,t}(1)",
            "incompatible repeated prime residue conditions are zero in both models",
            "does not claim",
            "Gate C verified finite-dimensional theorem",
        ],
        failures,
    )


def check_registry_and_boundary(failures: list[str]) -> None:
    """Check proposition registry and claim boundary know v0.9 is draft-only."""
    require_phrases(
        PROPOSITION_STATUS,
        [
            "`PCD-AK-TF-SLOW-CLT`",
            "`gate_c_verified`",
            "`PCD-AK-DIAG-ASM`",
            "`PCD-AK-FD-JOINT`",
            "Finite-dimensional fixed-angle Angular Erdos-Kac joint CLT",
            "`gate_c_verified`",
        ],
        failures,
    )
    require_phrases(
        CLAIM_BOUNDARY,
        [
            "v0.8",
            "Gate C verified",
            "v0.9",
            "finite-dimensional fixed-angle Gate C verified",
            "does not claim a finite-dimensional Gaussian field theorem",
        ],
        failures,
    )


def check_support_files(support_dir: Path, failures: list[str]) -> None:
    """Check deterministic v0.9 support output schema and invariants."""
    for name in [
        "support_manifest.json",
        "finite_dimensional_angular_ek_support.csv",
        "support_metadata.json",
    ]:
        require((support_dir / name).is_file(), f"missing support output: {name}", failures)

    manifest = json.loads((support_dir / "support_manifest.json").read_text(encoding="utf-8"))
    require(
        manifest.get("artifact_id") == "primeclock_dynamics_v0_9_finite_dimensional_angular_ek",
        "bad support artifact id",
        failures,
    )
    require(manifest.get("row_count") == 3, "unexpected support row count", failures)

    with (support_dir / "finite_dimensional_angular_ek_support.csv").open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    require(len(rows) == 3, "support CSV row count mismatch", failures)
    require(
        {row.get("angle_a") for row in rows} | {row.get("angle_b") for row in rows}
        == {"zero", "one_tenth", "sqrt2_mod1"},
        "angle labels mismatch",
        failures,
    )
    require(all(float(row["circular_distance"]) > 0 for row in rows), "angles must be distinct", failures)
    require(
        all(row.get("same_residue_primes_finite") == "True" for row in rows),
        "same-residue finiteness mismatch",
        failures,
    )
    require(
        all(float(row["same_residue_prime_safe_bound"]) >= 1 for row in rows),
        "safe same-residue prime bounds must be positive",
        failures,
    )
    require(
        all(row.get("normalized_covariance_target") == "off_diagonal_covariance/B_y^2 -> 0" for row in rows),
        "covariance target mismatch",
        failures,
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--support-dir", type=Path)
    args = parser.parse_args()

    failures: list[str] = []
    checks = [check_required_files, check_workflow, check_packet, check_registry_and_boundary]
    for check in checks:
        check(failures)

    if args.support_dir is None:
        with tempfile.TemporaryDirectory(prefix="pcd-v0-9-support-") as tmp_dir:
            support_dir = Path(tmp_dir)
            build_support(support_dir)
            check_support_files(support_dir, failures)
    else:
        check_support_files(args.support_dir, failures)

    if failures:
        print("check_finite_dimensional_angular_ek_packet: failed")
        for failure in failures:
            print(f"FAIL: {failure}")
        raise SystemExit(1)
    print(f"check_finite_dimensional_angular_ek_packet: checks={len(checks) + 1}, failed=0")


if __name__ == "__main__":
    main()
