#!/usr/bin/env python3
"""Check the v2.0.0 public artifact surface."""

from __future__ import annotations

import csv
import json
from pathlib import Path
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[2]
FROZEN_SOURCE_ROOT = ROOT / "artifacts/v2.0.0/source"
SOURCE_ROOT = FROZEN_SOURCE_ROOT if FROZEN_SOURCE_ROOT.is_dir() else ROOT
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "src"))

from experiments.akc.run_akc_v2_0_public_support import build_support

MANIFEST = ROOT / "experiments/_workflow/pcd_v2_0_public_artifact_manifest.json"
WORKFLOW = ROOT / "experiments/_workflow/pcd_v2_0_public_artifact.json"
README_PUBLIC_WORKFLOW = ROOT / "experiments/_workflow/README_V2_0_PUBLIC_ARTIFACT.md"
PUBLIC_MANIFEST = SOURCE_ROOT / "ARTIFACT_MANIFEST_v2_0_0.json"
RELEASE_NOTES = SOURCE_ROOT / "RELEASE_NOTES_v2_0_0.md"
README_PUBLIC = SOURCE_ROOT / "README.md"
CITATION = SOURCE_ROOT / "CITATION.cff"
MANUSCRIPT = SOURCE_ROOT / "paper/primeclock_dynamics_v2_0_public_manuscript.md"
CLAIM_BOUNDARY = SOURCE_ROOT / "docs/AKC_V2_0_PUBLIC_CLAIM_BOUNDARY.md"
BUILDER = ROOT / "scripts/build_v2_0_public_artifact.py"

FORBIDDEN_REQUIRED_FILES = {
    "README_V2_0_0.md",
    "CITATION_v2_0_0.cff",
    "paper/angular_kubilius_chaos_v2_0_gate_" + "c.md",
    "paper/angular_kubilius_chaos_v2_0_gate_" + "r.md",
    "experiments/_workflow/pcd_v2_0_akc_gate_" + "c.json",
    "experiments/_workflow/pcd_v2_0_akc_gate_" + "r.json",
    "experiments/_workflow/README_V2_0_GATE_C.md",
    "experiments/_workflow/README_V2_0_GATE_R.md",
    "experiments/_workflow/V2_0_GATE_C_STATUS.md",
    "experiments/_workflow/V2_0_GATE_" + "P_CANDIDATE_STATUS.md",
    "experiments/_workflow/pcd_v2_0_akc_gate_" + "p.json",
    "experiments/akc/_workflow/check_akc_v2_0_gate_" + "c.py",
    "experiments/akc/_workflow/check_akc_v2_0_gate_" + "r.py",
    "experiments/_workflow/check_v2_0_gate_" + "p_candidate.py",
}

FORBIDDEN_SURFACE_PHRASES = [
    "Gate " + "C candidate",
    "gate_" + "c_candidate",
    "Gate " + "R draft",
    "gate_" + "r_draft",
    "Gate " + "P Review",
    "Gate " + "P review",
    "gate_" + "p_candidate",
    "not " + "yet a public release",
    "public-preprint",
    "public candidate surface",
]


def first_existing(*paths: Path) -> Path:
    for path in paths:
        if path.is_file():
            return path
    return paths[0]


README_EFFECTIVE = first_existing(README_PUBLIC, ROOT / "README.md")
CITATION_EFFECTIVE = first_existing(CITATION, ROOT / "CITATION.cff")
PUBLIC_MANIFEST_EFFECTIVE = first_existing(PUBLIC_MANIFEST, ROOT / "ARTIFACT_MANIFEST_v2_0_0.json")
RELEASE_NOTES_EFFECTIVE = first_existing(RELEASE_NOTES, ROOT / "RELEASE_NOTES_v2_0_0.md")


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


def _load_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def check_required_files(failures: list[str]) -> None:
    for path in [
        MANIFEST,
        WORKFLOW,
        README_PUBLIC_WORKFLOW,
        PUBLIC_MANIFEST_EFFECTIVE,
        RELEASE_NOTES_EFFECTIVE,
        README_EFFECTIVE,
        CITATION_EFFECTIVE,
        MANUSCRIPT,
        CLAIM_BOUNDARY,
        BUILDER,
        ROOT / "experiments/akc/run_akc_v2_0_support_experiments.py",
        ROOT / "experiments/akc/run_akc_v2_0_public_support.py",
    ]:
        require(path.is_file(), f"missing required file: {path.relative_to(ROOT)}", failures)


def check_manifest_and_workflow(failures: list[str]) -> None:
    manifest = load_json(MANIFEST)
    public_manifest = load_json(PUBLIC_MANIFEST_EFFECTIVE)
    workflow = load_json(WORKFLOW)
    for loaded, name in [(manifest, "manifest"), (public_manifest, "public manifest"), (workflow, "workflow")]:
        require(isinstance(loaded, dict), f"{name} must be an object", failures)
    if not isinstance(manifest, dict) or not isinstance(public_manifest, dict):
        return

    artifact_id = "primeclock_dynamics_v2_0_0_angular_kubilius_chaos"
    require(manifest.get("artifact_id") == artifact_id, "bad manifest artifact id", failures)
    require(public_manifest.get("artifact_id") == artifact_id, "bad public manifest artifact id", failures)
    require(manifest.get("artifact_status") == "public_artifact", "bad manifest status", failures)
    require(public_manifest.get("artifact_status") == "public_artifact", "bad public manifest status", failures)
    claim_ids = {"PCD-AKC-MART", "PCD-AKC-QPOINT", "PCD-AKC-L2", "PCD-AKC-LIMIT", "PCD-AKC-TANGENT"}
    require(set(manifest.get("claim_ids", [])) == claim_ids, "bad claim ids", failures)
    require(set(public_manifest.get("claim_ids", [])) == claim_ids, "bad public claim ids", failures)
    required_files = set(manifest.get("required_files", []))
    require(FORBIDDEN_REQUIRED_FILES.isdisjoint(required_files), "manifest includes internal gate-history or aliased files", failures)
    for required in required_files:
        require((ROOT / required).is_file() or required in {"README.md", "CITATION.cff"}, f"required file missing: {required}", failures)
    for key in ["non_claims", "verification_commands", "excluded_from_public_artifact"]:
        require(isinstance(public_manifest.get(key), list), f"public manifest missing list: {key}", failures)

    if isinstance(workflow, dict):
        require(workflow.get("candidate_id") == "pcd_v2_0_public_artifact", "bad workflow id", failures)
        require(workflow.get("candidate_status") == "public_artifact", "bad workflow status", failures)
        require(workflow.get("public_release") is True, "public workflow must mark public_release=true", failures)
        gates = workflow.get("gates")
        require(isinstance(gates, dict) and {"quick", "bundle"} <= set(gates), "workflow missing gates", failures)


def check_text_surface(failures: list[str]) -> None:
    require_phrases(
        MANUSCRIPT,
        [
            "PrimeClock Dynamics v2.0.0: Angular Kubilius Chaos via Holomorphic Generating Functionals",
            "Status: v2.0.0 public artifact manuscript",
            "AKC-P3: Theorem A, Martingale Random Measures",
            "AKC-P4: Theorem B, q-Point Moment Formula",
            "AKC-P7: Theorem C, L2 Total-Mass Bound",
            "AKC-P8: Theorem D, Weak Convergence",
            "AKC-P9: Theorem E, Gaussian Tangent Recovery",
            "countable `Q`-vector subspace",
            "eventually bounded",
            "This public artifact manuscript does not claim",
        ],
        failures,
    )
    require_phrases(
        CLAIM_BOUNDARY,
        [
            "PrimeClock Dynamics v2.0.0 Public Claim Boundary",
            "complete-CRT finite-beta AKC",
            "PCD-AKC-L2",
            "PCD-AKC-LIMIT",
            "This public artifact does not claim",
        ],
        failures,
    )
    require_phrases(
        README_PUBLIC_WORKFLOW,
        [
            "PrimeClock Dynamics v2.0.0 Public Artifact",
            "pcd_v2_0_public_artifact",
            "excludes internal gate-history packets",
        ],
        failures,
    )
    require_phrases(
        README_EFFECTIVE,
        [
            "PrimeClock Dynamics v2.0.0",
            "Angular Kubilius Chaos via Holomorphic Generating Functionals",
            "Included Claim Surface",
            "Non-Claims",
        ],
        failures,
    )
    require_phrases(
        RELEASE_NOTES_EFFECTIVE,
        [
            "PrimeClock Dynamics v2.0.0 Release Notes",
            "finite-beta L2 total-mass bound",
            "weak convergence of random finite measures",
        ],
        failures,
    )


def check_support(failures: list[str]) -> None:
    with tempfile.TemporaryDirectory(prefix="pcd-v2-0-public-support-") as tmp_dir:
        out_dir = Path(tmp_dir)
        summary = build_support(out_dir)
        require(summary.get("profile") == "v2_0_akc_public_support", "bad support profile", failures)
        require(summary.get("experiment_count") == 6, "public support must contain six experiments", failures)
        require(summary.get("public_artifact_support") is True, "support must be public artifact support", failures)
        require(summary.get("public_release_claimed") is True, "support must mark public release claimed", failures)
        require((out_dir / "sha256.txt").is_file(), "support sha256 sidecar missing", failures)

        by_id = {int(item["id"]): item for item in summary["experiments"]}
        for experiment_id in range(1, 7):
            require(experiment_id in by_id, f"experiment {experiment_id} missing", failures)
            if experiment_id not in by_id:
                continue
            rows = _load_rows(out_dir / str(by_id[experiment_id]["file"]))
            require(len(rows) == by_id[experiment_id]["row_count"], f"experiment {experiment_id} row count mismatch", failures)
            require(all(row["experiment_id"] == str(experiment_id) for row in rows), f"experiment {experiment_id} id mismatch", failures)
            require(all(row["status"].startswith("public_") for row in rows), f"experiment {experiment_id} status must be public", failures)
            require(
                all(
                    "gate_" + "r_" not in row["status"]
                    and "gate_" + "c_" not in row["status"]
                    and "gate_" + "p_" not in row["status"]
                    for row in rows
                ),
                f"experiment {experiment_id} stale status",
                failures,
            )

        exp1 = _load_rows(out_dir / by_id[1]["file"])
        require(max(float(row["abs_error"]) for row in exp1) < 1e-12, "martingale support error too large", failures)
        exp2 = _load_rows(out_dir / by_id[2]["file"])
        require(max(float(row["abs_error"]) for row in exp2) < 1e-12, "q-point support error too large", failures)
        exp3 = _load_rows(out_dir / by_id[3]["file"])
        require(all(float(row["l2_total_mass"]) > 0 for row in exp3), "L2 support must be positive", failures)
        exp4 = _load_rows(out_dir / by_id[4]["file"])
        require(all(float(row["shell_integral_proxy"]) > 0 for row in exp4), "integrability support must be positive", failures)
        exp5 = _load_rows(out_dir / by_id[5]["file"])
        require(any(row["test_function"] == "one" for row in exp5), "weak support missing total mass test", failures)
        exp6 = _load_rows(out_dir / by_id[6]["file"])
        require(max(float(row["abs_error"]) for row in exp6) < 0.2, "Gaussian tangent support too loose", failures)


def check_forbidden_words(failures: list[str]) -> None:
    for path in [README_EFFECTIVE, RELEASE_NOTES_EFFECTIVE, MANUSCRIPT, CLAIM_BOUNDARY]:
        forbid_phrases(
            path,
            [
                *FORBIDDEN_SURFACE_PHRASES,
            ],
            failures,
        )


def main() -> None:
    failures: list[str] = []
    checks = [
        check_required_files,
        check_manifest_and_workflow,
        check_text_surface,
        check_support,
        check_forbidden_words,
    ]
    for check in checks:
        check(failures)
    if failures:
        print("check_v2_0_public_artifact: failed")
        for failure in failures:
            print(f"FAIL: {failure}")
        raise SystemExit(1)
    print(f"check_v2_0_public_artifact: checks={len(checks)}, failed=0")


if __name__ == "__main__":
    main()
