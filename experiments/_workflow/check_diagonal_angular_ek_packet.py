#!/usr/bin/env python3
"""Check the v0.8 diagonal Angular Erdos-Kac assembly record."""

from __future__ import annotations

import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "src"))

from experiments._workflow.build_diagonal_angular_ek_support import build_rows, build_support


PACKET = ROOT / "paper/diagonal_angular_erdos_kac_v0_8.md"
REVIEW_PACKET = ROOT / "experiments/_workflow/V0_8_GATE_R_REVIEW_PACKET.md"
PROPOSITION_STATUS = ROOT / "experiments/_workflow/PROPOSITION_STATUS.md"
CLAIM_BOUNDARY = ROOT / "docs/CLAIM_BOUNDARY.md"
WORKFLOW = ROOT / "experiments/_workflow/pcd_v0_8_diagonal_angular_ek_gate_r.json"
SUPPORT_BUILDER = ROOT / "experiments/_workflow/build_diagonal_angular_ek_support.py"


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
    """Check v0.8 draft files exist."""
    for path in [PACKET, REVIEW_PACKET, PROPOSITION_STATUS, CLAIM_BOUNDARY, WORKFLOW, SUPPORT_BUILDER]:
        require(path.is_file(), f"missing required file: {path.relative_to(ROOT)}", failures)


def check_workflow(failures: list[str]) -> None:
    """Check v0.8 workflow is a passed Gate R workflow."""
    data = json.loads(WORKFLOW.read_text(encoding="utf-8"))
    require(data.get("candidate_id") == "pcd_v0_8_diagonal_angular_ek_gate_r", "bad workflow id", failures)
    require(data.get("status") == "gate_r_passed", "bad workflow status", failures)
    require(data.get("public_release") is False, "workflow must not be public", failures)
    gates = data.get("gates")
    require(isinstance(gates, dict) and "quick" in gates, "workflow missing quick gate", failures)


def check_packet(failures: list[str]) -> None:
    """Check v0.8 paper wording and boundaries."""
    require_phrases(
        PACKET,
        [
            "PrimeClock Dynamics v0.8 Fixed-Angle Diagonal Angular Erdos-Kac Assembly Gate C Verified",
            "internal Gate C verified proof-route record",
            "v0.5 fixed-cutoff complete-CRT Angular CLT",
            "v0.6 slow-truncation finite-window moment bridge",
            "v0.7 all-angle L1 diagonal tail removal",
            "DAEK-1: Target Dyadic Statement",
            "(D_n(n, alpha) - A_{2N}) / B_{2N} => N(0,1)",
            "DAEK-2: Slow Truncation",
            "y(N)=floor(N^(1/log log N))",
            "DAEK-3: Dyadic Finite-Window Counting",
            "#{N < n <= 2N : n mod p = r_p(alpha) for every p in S}",
            "pi(y)^m/(N B_y^m) -> 0",
            "DAEK-4: Complete-CRT Gaussian Moment Convergence",
            "complete-CRT Gaussian moment convergence lemma",
            "O_r(B_y^(2-r)) -> 0",
            "E_CRT[((D_y-A_y)/B_y)^m] -> E[Z^m]",
            "DAEK-5: Truncated Finite-Window CLT",
            "PCD-AK-TF-SLOW-CLT",
            "internally Gate C verified",
            "DAEK-6: Tail Removal From v0.7",
            "T_y(n, alpha) / B_{2N} -> 0",
            "DAEK-7: Slutsky Assembly",
            "PCD-AK-DIAG-ASM",
            "DAEK-8: Dyadic Normalization Equivalence",
            "dyadic normalization equivalence lemma",
            "Gate C Support Evidence",
            "build_diagonal_angular_ek_support.py",
            "does not claim",
            "public theorem artifact",
        ],
        failures,
    )


def check_review_and_registry(failures: list[str]) -> None:
    """Check review packet and registry describe v0.8 as draft-only."""
    require_phrases(
        REVIEW_PACKET,
        [
            "v0.8 Gate R Review Packet",
            "not a Gate C candidate",
            "V0_8_GATE_R_PASS_RECORD.md",
            "paper/diagonal_angular_erdos_kac_v0_8.md",
            "v0.7 Gate C verified",
            "dyadic finite-window moment bridge",
            "does not claim that target as Gate C verified",
        ],
        failures,
    )
    require_phrases(
        PROPOSITION_STATUS,
        [
            "`PCD-AK-DIAG-ASM`",
            "Fixed-angle diagonal Angular Erdos-Kac assembly",
            "`gate_c_verified`",
            "paper/diagonal_angular_erdos_kac_v0_8.md",
            "`PCD-AK-TF-SLOW-CLT`",
        ],
        failures,
    )


def check_support_rows(failures: list[str]) -> None:
    """Check deterministic v0.8 support rows."""
    rows = build_rows()
    require(len(rows) == 3, "v0.8 support row count mismatch", failures)
    require([row["moment_order"] for row in rows] == [2, 3, 4], "moment orders mismatch", failures)
    require(all(row["truncation"] == "floor(N^(1/loglogN))" for row in rows), "truncation mismatch", failures)
    require(
        all(row["v0_6_fixed_order_budget_asymptotic"] for row in rows),
        "v0.6 asymptotic budget missing",
        failures,
    )
    require(any(row["finite_row_y_power_budget_below_one"] for row in rows), "expected at least one finite row below one", failures)
    require(all(float(row["y_power_over_N"]) >= 0.0 for row in rows), "y power budget must be nonnegative", failures)
    require(
        all(row["slutsky_tail_target"] == "T_y/B_2N -> 0 in probability" for row in rows),
        "Slutsky tail target mismatch",
        failures,
    )
    require(all(row["assembly_status"] == "gate_c_verified_support" for row in rows), "bad support status", failures)


def check_support_manifest(failures: list[str]) -> None:
    """Check support builder writes expected files."""
    import tempfile

    with tempfile.TemporaryDirectory(prefix="pcd_v0_8_support_") as tmp:
        manifest = build_support(Path(tmp))
        require(manifest["row_count"] == 3, "v0.8 support manifest row count mismatch", failures)
        require(
            manifest["artifact_id"] == "primeclock_dynamics_v0_8_diagonal_angular_ek",
            "bad v0.8 support artifact id",
            failures,
        )
        for filename in [
            "diagonal_angular_ek_support.csv",
            "support_manifest.json",
            "support_metadata.json",
        ]:
            require((Path(tmp) / filename).is_file(), f"missing support output: {filename}", failures)
    require_phrases(
        CLAIM_BOUNDARY,
        [
            "v0.8",
            "Gate C verified record",
            "fixed-angle diagonal Angular Erdos-Kac assembly route",
        ],
        failures,
    )


def main() -> None:
    failures: list[str] = []
    checks = [
        check_required_files,
        check_workflow,
        check_packet,
        check_review_and_registry,
        check_support_rows,
        check_support_manifest,
    ]
    for check in checks:
        check(failures)

    if failures:
        print("check_diagonal_angular_ek_packet: failed")
        for failure in failures:
            print(f"FAIL: {failure}")
        raise SystemExit(1)
    print(f"check_diagonal_angular_ek_packet: checks={len(checks)}, failed=0")


if __name__ == "__main__":
    main()
