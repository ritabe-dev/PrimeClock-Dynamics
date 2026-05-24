#!/usr/bin/env python3
"""Check the v3.5 integer-time transfer public artifact surface."""

from __future__ import annotations

import json
from pathlib import Path
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "src"))

from experiments.it.run_v3_5_public_support import write_outputs  # noqa: E402


def first_existing(*paths: Path) -> Path:
    for path in paths:
        if path.is_file():
            return path
    return paths[0]


README_EFFECTIVE = first_existing(ROOT / "README_V3_5_0_PUBLIC.md", ROOT / "README.md")
CITATION_EFFECTIVE = first_existing(ROOT / "CITATION_v3_5_0_PUBLIC.cff", ROOT / "CITATION.cff")


REQUIRED_FILES = [
    "RELEASE_NOTES_v3_5_0.md",
    "ARTIFACT_MANIFEST_v3_5_0.json",
    "docs/IT_V3_5_PUBLIC_CLAIM_BOUNDARY.md",
    "paper/primeclock_dynamics_v3_5_public_manuscript.md",
    "experiments/_workflow/README_V3_5_PUBLIC_ARTIFACT.md",
    "experiments/_workflow/pcd_v3_5_public_artifact.json",
    "experiments/it/run_v3_5_public_support.py",
    "src/prime_clock_dynamics/integer_time_transfer.py",
]


def require(condition: bool, message: str, failures: list[str]) -> None:
    if not condition:
        failures.append(message)


def require_phrases(path: Path, phrases: list[str], failures: list[str]) -> None:
    text = path.read_text(encoding="utf-8")
    for phrase in phrases:
        require(phrase in text, f"{path.relative_to(ROOT)} missing phrase: {phrase}", failures)


def check_required_files(failures: list[str]) -> None:
    require(README_EFFECTIVE.is_file(), "missing required file: README.md", failures)
    require(CITATION_EFFECTIVE.is_file(), "missing required file: CITATION.cff", failures)
    for relative in REQUIRED_FILES:
        require((ROOT / relative).is_file(), f"missing required file: {relative}", failures)


def check_paper_and_boundary(failures: list[str]) -> None:
    require_phrases(
        ROOT / "paper/primeclock_dynamics_v3_5_public_manuscript.md",
        [
            "Slow-Cutoff Integer-Time Transfer",
            "Status: public artifact manuscript",
            "PCD-IT-TV",
            "PCD-IT-DIST",
            "PCD-IT-MOM-m",
            "total variation",
            "does not claim",
            "full diagonal Mertens transfer",
            "diagnostic only",
        ],
        failures,
    )
    require_phrases(
        ROOT / "docs/IT_V3_5_PUBLIC_CLAIM_BOUNDARY.md",
        [
            "Status: public artifact claim boundary",
            "PCD-IT-TV",
            "PCD-IT-DIST",
            "PCD-IT-MOM-m",
            "distributional diagonal transfer",
            "conductor-tail theorem",
        ],
        failures,
    )


def check_workflow(failures: list[str]) -> None:
    workflow = json.loads(
        (
            ROOT / "experiments/_workflow/pcd_v3_5_public_artifact.json"
        ).read_text(encoding="utf-8")
    )
    require(workflow.get("candidate_id") == "pcd_v3_5_public_artifact", "bad workflow id", failures)
    require(workflow.get("status") == "public_artifact", "bad workflow status", failures)
    require(workflow.get("public_release") is True, "workflow must be public", failures)
    gates = workflow.get("gates", {})
    require({"quick", "support", "bundle"}.issubset(gates), "workflow missing required gates", failures)


def check_support(failures: list[str]) -> None:
    with tempfile.TemporaryDirectory(prefix="pcd-it-v3-5-public-check-") as tmp_dir:
        summary = write_outputs(Path(tmp_dir))
    require(summary["experiment_count"] == 5, "wrong experiment count", failures)
    require(summary["row_count"] == 31, "wrong support row count", failures)
    require(summary["public_artifact_support"] is True, "support must be public support", failures)
    require(summary["public_release_claimed"] is True, "support must mark public release", failures)
    require(summary["doi_claimed"] is False, "support must not claim DOI", failures)
    require(summary["zenodo_claimed"] is False, "support must not claim Zenodo", failures)
    require(summary["full_diagonal_claimed"] is False, "support must not claim full diagonal", failures)
    require(summary["distributional_diagonal_claimed"] is False, "support must not claim diagonal distribution", failures)
    require(summary["conductor_tail_theorem_claimed"] is False, "support must not claim conductor theorem", failures)
    require(summary["all_tv_bounds_passed"] is True, "TV bounds failed", failures)
    require(summary["all_bounded_test_bounds_passed"] is True, "bounded-test bounds failed", failures)
    require(summary["all_moment_bounds_passed"] is True, "moment bounds failed", failures)
    with tempfile.TemporaryDirectory(prefix="pcd-it-v3-5-public-labels-") as tmp_dir:
        out_dir = Path(tmp_dir)
        write_outputs(out_dir)
        for path in out_dir.glob("*.csv"):
            text = path.read_text(encoding="utf-8")
            require("public_" in text, f"{path.name} missing public status", failures)
            require("gate_" + "p_" not in text, f"{path.name} contains stale Gate P status", failures)
            require("gate_" + "c_" not in text, f"{path.name} contains stale Gate C status", failures)
            require("gate_" + "r_" not in text, f"{path.name} contains stale Gate R status", failures)


def check_forbidden_public_words(failures: list[str]) -> None:
    forbidden = [
        "Gate " + "P review candidate",
        "internal Gate P",
        "not " + "public",
        "not " + "DOI/Zenodo",
        "gate_" + "p_",
        "gate_" + "c_",
        "gate_" + "r_",
    ]
    public_files = [
        README_EFFECTIVE,
        ROOT / "RELEASE_NOTES_v3_5_0.md",
        ROOT / "docs/IT_V3_5_PUBLIC_CLAIM_BOUNDARY.md",
        ROOT / "paper/primeclock_dynamics_v3_5_public_manuscript.md",
        ROOT / "experiments/_workflow/README_V3_5_PUBLIC_ARTIFACT.md",
    ]
    for path in public_files:
        text = path.read_text(encoding="utf-8")
        for phrase in forbidden:
            require(phrase not in text, f"{path.relative_to(ROOT)} contains forbidden phrase: {phrase}", failures)


def main() -> None:
    failures: list[str] = []
    checks = [
        check_required_files,
        check_paper_and_boundary,
        check_workflow,
        check_support,
        check_forbidden_public_words,
    ]
    for check in checks:
        check(failures)
    if failures:
        print("check_v3_5_public_artifact: failed")
        for failure in failures:
            print(f"FAIL: {failure}")
        raise SystemExit(1)
    print(f"check_v3_5_public_artifact: checks={len(checks)}, failed=0")


if __name__ == "__main__":
    main()
