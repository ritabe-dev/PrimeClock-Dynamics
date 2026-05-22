#!/usr/bin/env python3
"""Check the v1.1 public artifact surface."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]

SOURCE_ALIASES = {
    "README.md": "README_V1_1_0_PUBLIC.md",
    "RELEASE_NOTES_v1_1_0.md": "RELEASE_NOTES_v1_1_0_PUBLIC.md",
    "CITATION.cff": "CITATION_v1_1_0_PUBLIC.cff",
    "ARTIFACT_MANIFEST_v1_1_0.json": "ARTIFACT_MANIFEST_v1_1_0_PUBLIC.json",
}


def resolve_public(relative: str) -> Path:
    alias = SOURCE_ALIASES.get(relative)
    if alias and (ROOT / alias).is_file():
        return ROOT / alias
    return ROOT / relative


MANIFEST = ROOT / "experiments/_workflow/pcd_v1_1_public_artifact_manifest.json"
WORKFLOW = ROOT / "experiments/_workflow/pcd_v1_1_public_artifact.json"
README_PUBLIC_WORKFLOW = ROOT / "experiments/_workflow/README_V1_1_PUBLIC_ARTIFACT.md"
PUBLIC_MANIFEST = resolve_public("ARTIFACT_MANIFEST_v1_1_0.json")
RELEASE_NOTES = resolve_public("RELEASE_NOTES_v1_1_0.md")
README_PUBLIC = resolve_public("README.md")
CITATION = resolve_public("CITATION.cff")
MANUSCRIPT = ROOT / "paper/primeclock_dynamics_v1_1_manuscript.md"
CLAIM_BOUNDARY = ROOT / "docs/SAGF_CLAIM_BOUNDARY.md"
MATH_SPEC = ROOT / "docs/SAGF_MATH_SPEC.md"
RELATED_WORK = ROOT / "docs/SAGF_RELATED_WORK.md"

FORBIDDEN_REQUIRED_FILES = {
    "README_V1_1_0.md",
    "README_V1_1_0_PUBLIC.md",
    "CITATION_v1_1_0.cff",
    "CITATION_v1_1_0_PUBLIC.cff",
    "RELEASE_NOTES_v1_1_0_PUBLIC.md",
    "ARTIFACT_MANIFEST_v1_1_0_PUBLIC.json",
    "docs/AKC_PROGRAM.md",
    "docs/AKC_PUBLICATION_PLAN.md",
    "docs/AKC_VERSION_SURFACE_MAP.md",
    "docs/internal/V1_0_PROOF_PROGRAM_LOCK.md",
    "experiments/_workflow/GATE_R_PROGRAM_STATUS.md",
    "experiments/_workflow/PROPOSITION_STATUS.md",
    "experiments/_workflow/V1_1_GATE_C_STATUS.md",
    "experiments/_workflow/V1_1_GATE_P_" + "CANDIDATE_STATUS.md",
    "experiments/_workflow/V1_1_GATE_R_REVIEW_PACKET.md",
    "experiments/_workflow/V1_1_GATE_R_REVIEW_REQUEST_DRAFT.md",
    "paper/primeclock_dynamics_v1_1_preprint.md",
    "paper/shrinking_angle_gaussian_field_v1_1_gate_c.md",
    "paper/angular_kubilius_chaos_v2_0_gate_r.md",
}

FORBIDDEN_PUBLIC_PHRASES = [
    "Gate P " + "Review",
    "Gate P " + "review",
    "not yet a public " + "release",
    "gate_p_" + "candidate",
    "Gate C " + "candidate",
    "gate_c_" + "candidate",
    "public-" + "preprint",
    "public " + "candidate surface",
]


def require(condition: bool, message: str, failures: list[str]) -> None:
    if not condition:
        failures.append(message)


def load_json(path: Path) -> object:
    return json.loads(path.read_text(encoding="utf-8"))


def require_phrases(path: Path, phrases: list[str], failures: list[str]) -> None:
    text = path.read_text(encoding="utf-8")
    for phrase in phrases:
        require(phrase in text, f"{path.relative_to(ROOT)} missing phrase: {phrase}", failures)


def forbid_phrases(path: Path, phrases: list[str], failures: list[str]) -> None:
    text = path.read_text(encoding="utf-8")
    for phrase in phrases:
        require(phrase not in text, f"{path.relative_to(ROOT)} contains forbidden phrase: {phrase}", failures)


def check_required_files(failures: list[str]) -> None:
    for path in [
        MANIFEST,
        WORKFLOW,
        README_PUBLIC_WORKFLOW,
        PUBLIC_MANIFEST,
        RELEASE_NOTES,
        README_PUBLIC,
        CITATION,
        MANUSCRIPT,
        CLAIM_BOUNDARY,
        MATH_SPEC,
        RELATED_WORK,
    ]:
        require(path.is_file(), f"missing required file: {path.relative_to(ROOT)}", failures)


def check_manifest_and_workflow(failures: list[str]) -> None:
    manifest = load_json(MANIFEST)
    public_manifest = load_json(PUBLIC_MANIFEST)
    workflow = load_json(WORKFLOW)
    for loaded, name in [(manifest, "manifest"), (public_manifest, "public manifest"), (workflow, "workflow")]:
        require(isinstance(loaded, dict), f"{name} must be an object", failures)
    if not isinstance(manifest, dict) or not isinstance(public_manifest, dict):
        return

    artifact_id = "primeclock_dynamics_v1_1_0_shrinking_angle_gaussian_field"
    require(manifest.get("artifact_id") == artifact_id, "bad manifest artifact id", failures)
    require(public_manifest.get("artifact_id") == artifact_id, "bad public manifest artifact id", failures)
    require(manifest.get("artifact_status") == "public_artifact", "bad manifest status", failures)
    require(public_manifest.get("artifact_status") == "public_artifact", "bad public manifest status", failures)
    require(set(manifest.get("claim_ids", [])) == {"PCD-AKC-SAGF-CRT", "PCD-AKC-SAGF-ZERO-RAY"}, "bad claim ids", failures)
    required_files = set(manifest.get("required_files", []))
    require(FORBIDDEN_REQUIRED_FILES.isdisjoint(required_files), "manifest includes internal or aliased files", failures)
    for required in required_files:
        require((ROOT / required).is_file() or required in SOURCE_ALIASES, f"required file missing: {required}", failures)
    for key in ["non_claims", "verification_commands", "excluded_from_public_artifact"]:
        require(isinstance(public_manifest.get(key), list), f"public manifest missing list: {key}", failures)

    if isinstance(workflow, dict):
        require(workflow.get("artifact_id") == artifact_id, "bad workflow id", failures)
        require(workflow.get("artifact_status") == "public_artifact", "bad workflow status", failures)
        gates = workflow.get("gates")
        require(isinstance(gates, dict) and {"quick", "bundle"} <= set(gates), "workflow missing gates", failures)


def check_text_surface(failures: list[str]) -> None:
    require_phrases(
        MANUSCRIPT,
        [
            "PrimeClock Dynamics v1.1.0: A Shrinking-Angle Gaussian Field",
            "Status: v1.1.0 public research artifact manuscript",
            "Theorem A: kernel-conditioned complete-CRT Gaussian limit",
            "K_x(alpha_i(x), alpha_j(x)) / B_x^2 -> kappa_ij",
            "Zero-Ray Shrinking Corollary",
            "K_x(0, delta_x) / B_x^2 -> theta",
            "This manuscript does not claim integer-time transfer",
        ],
        failures,
    )
    require_phrases(
        CLAIM_BOUNDARY,
        [
            "Shrinking-Angle Gaussian Field Claim Boundary",
            "complete-CRT kernel-conditioned finite-dimensional Gaussian convergence",
            "explicit zero-ray shrinking-angle Gaussian corollary",
            "This public artifact does not claim",
            "Angular Kubilius Chaos is future work",
        ],
        failures,
    )
    require_phrases(
        MATH_SPEC,
        [
            "Shrinking-Angle Gaussian Field Math Specification",
            "The v1.1 theorem is in the complete-CRT model",
            "K_x(alpha, beta)",
            "K_x(0, delta_x) / B_x^2 -> theta",
        ],
        failures,
    )
    require_phrases(
        RELATED_WORK,
        [
            "Kubilius probabilistic model",
            "not standard Gaussian Multiplicative Chaos",
            "General distance-only kernel laws are not claimed",
        ],
        failures,
    )
    require_phrases(
        README_PUBLIC_WORKFLOW,
        [
            "PrimeClock Dynamics v1.1.0 Public Artifact",
            "primeclock_dynamics_v1_1_0_shrinking_angle_gaussian_field",
            "paper/primeclock_dynamics_v1_1_manuscript.md",
        ],
        failures,
    )
    require_phrases(
        README_PUBLIC,
        [
            "PrimeClock Dynamics v1.1.0",
            "A Shrinking-Angle Gaussian Field",
            "Claim Surface",
            "Non-Claims",
        ],
        failures,
    )
    require_phrases(
        RELEASE_NOTES,
        [
            "v1.1.0 Release Notes",
            "Complete-CRT collision kernel",
            "Explicit zero-ray shrinking-angle corollary",
        ],
        failures,
    )
    require_phrases(
        CITATION,
        [
            "PrimeClock Dynamics v1.1.0 public research artifact",
            "not peer reviewed",
        ],
        failures,
    )


def check_public_wording(failures: list[str]) -> None:
    for path in [README_PUBLIC, RELEASE_NOTES, MANUSCRIPT, README_PUBLIC_WORKFLOW, PUBLIC_MANIFEST, MANIFEST, WORKFLOW]:
        forbid_phrases(path, FORBIDDEN_PUBLIC_PHRASES, failures)
    for path in [CLAIM_BOUNDARY, MATH_SPEC, RELATED_WORK]:
        forbid_phrases(path, FORBIDDEN_PUBLIC_PHRASES, failures)


def main() -> None:
    failures: list[str] = []
    checks = [check_required_files, check_manifest_and_workflow, check_text_surface, check_public_wording]
    for check in checks:
        check(failures)
    if failures:
        print("check_v1_1_public_artifact: failed")
        for failure in failures:
            print(f"FAIL: {failure}")
        raise SystemExit(1)
    print(f"check_v1_1_public_artifact: checks={len(checks)}, failed=0")


if __name__ == "__main__":
    main()
