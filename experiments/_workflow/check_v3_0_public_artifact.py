#!/usr/bin/env python3
"""Check the v3.0 Mertens-boundary public artifact surface."""

from __future__ import annotations

import csv
import json
from pathlib import Path
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "src"))

from experiments.mb.run_mb_v3_0_public_support import build_support


def first_existing(*paths: Path) -> Path:
    for path in paths:
        if path.is_file():
            return path
    return paths[0]


MANIFEST = first_existing(ROOT / "ARTIFACT_MANIFEST_v3_0_0_PUBLIC.json", ROOT / "ARTIFACT_MANIFEST_v3_0_0.json")
WORKFLOW = ROOT / "experiments/_workflow/pcd_v3_0_public_artifact.json"
README_WORKFLOW = ROOT / "experiments/_workflow/README_V3_0_PUBLIC_ARTIFACT.md"
CANDIDATE_README = first_existing(ROOT / "README_V3_0_0_RELEASE.md", ROOT / "README.md")
RELEASE_NOTES = first_existing(ROOT / "RELEASE_NOTES_v3_0_0_PUBLIC.md", ROOT / "RELEASE_NOTES_v3_0_0.md")
CANDIDATE_CITATION = first_existing(ROOT / "CITATION_v3_0_0_RELEASE.cff", ROOT / "CITATION.cff")
CLAIM_BOUNDARY = first_existing(
    ROOT / "docs/MB_V3_0_RELEASE_CLAIM_BOUNDARY.md",
    ROOT / "docs/MB_V3_0_PUBLIC_CLAIM_BOUNDARY.md",
)
MATH_SPEC = ROOT / "docs/MB_V3_0_MATH_SPEC.md"
MANUSCRIPT = first_existing(
    ROOT / "paper/primeclock_dynamics_v3_0_release_manuscript.md",
    ROOT / "paper/primeclock_dynamics_v3_0_public_manuscript.md",
)
SUPPORT_RUNNER = ROOT / "experiments/mb/run_mb_v3_0_public_support.py"
BUILDER = ROOT / "scripts/build_v3_0_public_artifact.py"

CLAIM_IDS = {
    "PCD-MB-MART",
    "PCD-MB-QPOINT",
    "PCD-MB-L2",
    "PCD-MB-LIMIT",
    "PCD-MB-FB-ENDPOINT",
}

FORBIDDEN_SURFACE_PHRASES = [
    "Gate R route-review manuscript",
    "Gate C theorem-candidate manuscript",
    "Target Theorem",
    "gate_r_",
    "gate_c_",
    "public release: yes",
    "DOI: yes",
    "Zenodo: yes",
]


README_EFFECTIVE = first_existing(CANDIDATE_README, ROOT / "README.md")
CITATION_EFFECTIVE = first_existing(CANDIDATE_CITATION, ROOT / "CITATION.cff")


def require(condition: bool, message: str, failures: list[str]) -> None:
    if not condition:
        failures.append(message)


def require_phrases(path: Path, phrases: list[str], failures: list[str]) -> None:
    text = path.read_text(encoding="utf-8")
    for phrase in phrases:
        require(phrase in text, f"{path.relative_to(ROOT)} missing phrase: {phrase}", failures)


def forbid_phrases(path: Path, phrases: list[str], failures: list[str]) -> None:
    text = path.read_text(encoding="utf-8")
    for phrase in phrases:
        require(phrase not in text, f"{path.relative_to(ROOT)} contains forbidden phrase: {phrase}", failures)


def load_json(path: Path) -> object:
    return json.loads(path.read_text(encoding="utf-8"))


def load_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def check_required_files(failures: list[str]) -> None:
    for path in [
        MANIFEST,
        WORKFLOW,
        README_WORKFLOW,
        README_EFFECTIVE,
        RELEASE_NOTES,
        CITATION_EFFECTIVE,
        CLAIM_BOUNDARY,
        MATH_SPEC,
        MANUSCRIPT,
        SUPPORT_RUNNER,
        BUILDER,
    ]:
        require(path.is_file(), f"missing required file: {path.relative_to(ROOT)}", failures)


def check_manifest_and_workflow(failures: list[str]) -> None:
    manifest = load_json(MANIFEST)
    workflow = load_json(WORKFLOW)
    require(isinstance(manifest, dict), "manifest must be an object", failures)
    require(isinstance(workflow, dict), "workflow must be an object", failures)
    if isinstance(manifest, dict):
        require(manifest.get("artifact_id") == "primeclock_dynamics_v3_0_0_mertens_boundary", "bad manifest id", failures)
        require(manifest.get("artifact_status") == "public_artifact", "bad manifest status", failures)
        require(set(manifest.get("claim_ids", [])) == CLAIM_IDS, "bad claim ids", failures)
        require("not DOI" not in manifest.get("non_claims", []), "public manifest must not claim DOI", failures)
        require("not Zenodo" not in manifest.get("non_claims", []), "public manifest must not claim Zenodo", failures)
    if isinstance(workflow, dict):
        require(workflow.get("candidate_id") == "pcd_v3_0_public_artifact", "bad workflow id", failures)
        require(workflow.get("candidate_status") == "public_artifact", "bad workflow status", failures)
        require(workflow.get("public_release") is True, "public artifact must mark public_release", failures)
        gates = workflow.get("gates", {})
        require(isinstance(gates, dict) and {"quick", "support", "bundle"} <= set(gates), "workflow missing gates", failures)


def check_text_surface(failures: list[str]) -> None:
    require_phrases(
        README_EFFECTIVE,
        [
            "PrimeClock Dynamics v3.0.0",
            "The Mertens Boundary of Angular Kubilius Chaos",
            "Included Claim Surface",
            "v3.5 soft integer-time transfer",
        ],
        failures,
    )
    require_phrases(
        CLAIM_BOUNDARY,
        [
            "PrimeClock Dynamics v3.0.0 Public Claim Boundary",
            "Gate C and Gate P reviews passed",
            *sorted(CLAIM_IDS),
            "Boundary Convention",
                    ],
        failures,
    )
    require_phrases(
        MANUSCRIPT,
        [
            "PrimeClock Dynamics v3.0.0",
            "Status: v3.0.0 public artifact manuscript",
            "MB-C3: Theorem A, Martingale Random Measures",
            "MB-C4: Theorem B, q-Point Hard Local Factor",
            "MB-C7: Theorem C, L2 Total-Mass Bound",
            "The diagonal case `alpha=gamma`",
            "MB-C8: Theorem D, Weak Convergence",
            "controlled by the limiting total mass",
            "MB-C9: Theorem E, Fixed-Cutoff beta Endpoint Compatibility",
        ],
        failures,
    )
    require_phrases(
        RELEASE_NOTES,
        [
            "Public Artifact Release Notes",
            "finite L2 total-mass bound",
            "weak convergence of complete-CRT Mertens-boundary random finite measures",
        ],
        failures,
    )
    for path in [README_EFFECTIVE, RELEASE_NOTES, CLAIM_BOUNDARY, MANUSCRIPT]:
        forbid_phrases(path, FORBIDDEN_SURFACE_PHRASES, failures)


def check_support(failures: list[str]) -> None:
    with tempfile.TemporaryDirectory(prefix="pcd-mb-v3-gate-p-") as tmp_dir:
        out_dir = Path(tmp_dir)
        summary = build_support(out_dir)
        require(summary.get("profile") == "v3_0_mertens_boundary_public_support", "bad support profile", failures)
        require(summary.get("experiment_count") == 6, "public support must contain six experiments", failures)
        require(summary.get("public_artifact_support") is True, "support must mark public artifact", failures)
        require(summary.get("public_release_claimed") is True, "support must mark public release", failures)
        require(summary.get("doi_claimed") is False, "support must not claim DOI", failures)
        require(summary.get("zenodo_claimed") is False, "support must not claim Zenodo", failures)
        experiment_files = sorted(out_dir.glob("experiment_*.csv"))
        require(len(experiment_files) == 6, "expected six public experiment CSV files", failures)
        for path in experiment_files:
            rows = load_rows(path)
            require(rows, f"empty support CSV: {path.name}", failures)
            statuses = {row.get("status", "") for row in rows}
            require(all(status.startswith("public_") for status in statuses), f"public status must use public_* labels: {path.name}", failures)
            if "negative_beta_endpoint" in path.name:
                require("finite_beta_total_mass_exact_polynomial" in rows[0], "negative-beta support must use exact polynomial", failures)
                require(all("grid" not in key for key in rows[0]), "negative-beta support must not expose grid columns", failures)
        require((out_dir / "sha256.txt").is_file(), "support sha256 missing", failures)


def main() -> None:
    failures: list[str] = []
    checks = [
        check_required_files,
        check_manifest_and_workflow,
        check_text_surface,
        check_support,
    ]
    for check in checks:
        check(failures)
    if failures:
        print("check_v3_0_public_artifact: failed")
        for failure in failures:
            print(f"FAIL: {failure}")
        raise SystemExit(1)
    print(f"check_v3_0_public_artifact: checks={len(checks)}, failed=0")


if __name__ == "__main__":
    main()
