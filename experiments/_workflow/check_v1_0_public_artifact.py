#!/usr/bin/env python3
"""Check the v1.0 public artifact surface."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
FROZEN_SOURCE_ROOT = ROOT / "artifacts/v1.0.0/source"
PUBLIC_ROOT = FROZEN_SOURCE_ROOT if FROZEN_SOURCE_ROOT.is_dir() else ROOT
MANIFEST = PUBLIC_ROOT / "experiments/_workflow/pcd_v1_0_public_artifact_manifest.json"
WORKFLOW = PUBLIC_ROOT / "experiments/_workflow/pcd_v1_0_public_artifact.json"
README_GATE_P = PUBLIC_ROOT / "experiments/_workflow/README_V1_0_PUBLIC_ARTIFACT.md"
STATUS = PUBLIC_ROOT / "experiments/_workflow/README_V1_0_PUBLIC_ARTIFACT.md"
PUBLIC_MANIFEST = PUBLIC_ROOT / "ARTIFACT_MANIFEST_v1_0_0.json"
RELEASE_NOTES = PUBLIC_ROOT / "RELEASE_NOTES_v1_0_0.md"
PREPRINT = PUBLIC_ROOT / "paper/primeclock_dynamics_v1_0_preprint.md"
CLAIM_BOUNDARY = PUBLIC_ROOT / "docs/CLAIM_BOUNDARY.md"
CITATION = PUBLIC_ROOT / "CITATION.cff"

FORBIDDEN_REQUIRED_FILES = {
    "docs/ROADMAP.md",
    "docs/internal/V1_0_PROOF_PROGRAM_LOCK.md",
    "experiments/_workflow/GATE_R_PROGRAM_STATUS.md",
    "experiments/_workflow/PROPOSITION_STATUS.md",
    "experiments/_workflow/V1_0_GATE_C_PASS_RECORD.md",
    "experiments/_workflow/V1_0_GATE_C_CANDIDATE_STATUS.md",
    "paper/integrated_angular_ek_mertens_v1_0.md",
    "paper/diagonal_bridge_packet_v0_3.md",
    "paper/random_nonrandom_packet_v0_4.md",
}


def require(condition: bool, message: str, failures: list[str]) -> None:
    """Append ``message`` when ``condition`` is false."""
    if not condition:
        failures.append(message)


def load_json(path: Path) -> object:
    """Load JSON from ``path``."""
    return json.loads(path.read_text(encoding="utf-8"))


def require_phrases(path: Path, phrases: list[str], failures: list[str]) -> None:
    """Check that ``path`` contains all required phrases."""
    text = path.read_text(encoding="utf-8")
    for phrase in phrases:
        require(phrase in text, f"{path.relative_to(PUBLIC_ROOT)} missing phrase: {phrase}", failures)


def check_required_files(failures: list[str]) -> None:
    """Check the public artifact entry files exist."""
    for path in [
        MANIFEST,
        WORKFLOW,
        README_GATE_P,
        STATUS,
        PUBLIC_MANIFEST,
        RELEASE_NOTES,
        PREPRINT,
        CLAIM_BOUNDARY,
        CITATION,
    ]:
        require(path.is_file(), f"missing required file: {path.relative_to(ROOT)}", failures)


def check_manifest_and_workflow(failures: list[str]) -> None:
    """Check the public-preprint manifest and workflow shape."""
    manifest = load_json(MANIFEST)
    public_manifest = load_json(PUBLIC_MANIFEST)
    workflow = load_json(WORKFLOW)
    for loaded, name in [(manifest, "manifest"), (public_manifest, "public manifest"), (workflow, "workflow")]:
        require(isinstance(loaded, dict), f"{name} must be an object", failures)
    if not isinstance(manifest, dict) or not isinstance(public_manifest, dict):
        return
    require(
        manifest.get("artifact_id") == "primeclock_dynamics_v1_0_0_angular_ek_fixed_cutoff_mertens",
        "bad manifest artifact id",
        failures,
    )
    require(manifest.get("artifact_status") == "public_artifact", "bad manifest status", failures)
    require(public_manifest == manifest, "root public manifest and workflow manifest differ", failures)
    required_ids = {
        "PCD-AK-FC-CLT",
        "PCD-AK-TF-MOMENT",
        "PCD-AK-DT-L1",
        "PCD-AK-DT-SLUT",
        "PCD-AK-TF-SLOW-CLT",
        "PCD-AK-DIAG-ASM",
        "PCD-AK-FD-JOINT",
        "PCD-MG-1",
    }
    require(required_ids <= set(manifest.get("claim_ids", [])), "missing claim ids", failures)
    required_files = set(manifest.get("required_files", []))
    require(
        FORBIDDEN_REQUIRED_FILES.isdisjoint(required_files),
        "manifest includes internal or diagnostic files",
        failures,
    )
    for required in required_files:
        require((PUBLIC_ROOT / required).is_file(), f"required file missing: {required}", failures)
    for key in ["non_claims", "verification_commands", "excluded_from_public_artifact"]:
        require(isinstance(manifest.get(key), list), f"manifest missing list: {key}", failures)
    if isinstance(workflow, dict):
        require(workflow.get("artifact_id") == "primeclock_dynamics_v1_0_0_angular_ek_fixed_cutoff_mertens", "bad workflow artifact id", failures)
        require(workflow.get("artifact_status") == "public_artifact", "bad workflow status", failures)
        gates = workflow.get("gates")
        require(isinstance(gates, dict) and {"quick", "bundle"} <= set(gates), "workflow missing gates", failures)


def check_text_surface(failures: list[str]) -> None:
    """Check public-facing wording and boundaries."""
    require_phrases(
        PREPRINT,
        [
            "PrimeClock Dynamics: An Angular Erdos-Kac Theorem",
            "Status: v1.0 public research artifact and preprint-style manuscript",
            "Theorem A: finite-dimensional fixed-angle Angular Erdos-Kac theorem",
            "D_n(n,0)=omega(n)",
            "consistent with the classical Erdos-Kac theorem",
            "not presented as a new strengthening",
            "Fixed-Cutoff Geometric Mertens Identity",
            "not a diagonal Mertens law",
            "not a new proof of Mertens' theorem",
            "## 10. References",
        ],
        failures,
    )
    require_phrases(
        CLAIM_BOUNDARY,
        [
            "PrimeClock Dynamics v1.0.0 is a public research artifact",
            "finite-dimensional fixed-angle Angular Erdos-Kac theorem",
            "fixed-cutoff CRT uncovered-average identity",
            "corresponding dyadic",
            "not presented as a new strengthening",
            "diagonal Mertens uncovered-measure law",
        ],
        failures,
    )
    require_phrases(
        RELEASE_NOTES,
        [
            "v1.0.0 Release Notes",
            "finite-dimensional fixed-angle Angular Erdos-Kac theorem",
            "fixed-cutoff CRT uncovered-average identity",
            "not uniform-in-alpha convergence",
            "not a new proof of Mertens' theorem",
        ],
        failures,
    )
    require_phrases(
        README_GATE_P,
        [
            "PrimeClock Dynamics v1.0.0 Public Artifact",
            "primeclock_dynamics_v1_0_0_angular_ek_fixed_cutoff_mertens",
            "paper/primeclock_dynamics_v1_0_preprint.md",
            "check_v1_0_public_artifact.py",
        ],
        failures,
    )
    require_phrases(
        STATUS,
        [
            "public research artifact",
            "not peer reviewed",
            "not a DOI artifact",
        ],
        failures,
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.parse_args()

    failures: list[str] = []
    checks = [check_required_files, check_manifest_and_workflow, check_text_surface]
    for check in checks:
        check(failures)

    if failures:
        print("check_v1_0_public_artifact: failed")
        for failure in failures:
            print(f"FAIL: {failure}")
        raise SystemExit(1)
    print(f"check_v1_0_public_artifact: checks={len(checks)}, failed=0")


if __name__ == "__main__":
    main()
