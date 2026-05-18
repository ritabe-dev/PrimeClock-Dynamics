#!/usr/bin/env python3
"""Check the v0.2.0 public artifact verification surface."""

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

from experiments._workflow.build_v0_2_support import ARTIFACT_ID, build_support


MANIFEST = ROOT / "experiments/_workflow/v0_2_verification_manifest.json"
WORKFLOW = ROOT / "experiments/_workflow/v0_2_verification_workflow.json"
PUBLIC_MANIFEST = ROOT / "ARTIFACT_MANIFEST_v0_2_0.json"
PACKET = ROOT / "paper/fixed_cutoff_foundation_v0_2_0.md"
FORBIDDEN_PUBLIC_FILES = {
    "docs/ROADMAP.md",
    "experiments/_workflow/V0_2_" + "VERIFICATION_RECORD.md",
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
        require(phrase in text, f"{path.relative_to(ROOT)} missing phrase: {phrase}", failures)


def check_manifest(failures: list[str]) -> None:
    """Check public verification manifest shape and required file list."""
    require(MANIFEST.is_file(), "missing public verification manifest", failures)
    require(WORKFLOW.is_file(), "missing public verification workflow", failures)
    manifest = load_json(MANIFEST)
    require(isinstance(manifest, dict), "manifest must be an object", failures)
    if not isinstance(manifest, dict):
        return
    require(manifest.get("artifact_id") == ARTIFACT_ID, "bad artifact id", failures)
    require(manifest.get("artifact_status") == "public_artifact", "bad artifact status", failures)
    for key in ["non_claims", "claim_ids", "required_files", "support_outputs"]:
        require(isinstance(manifest.get(key), list), f"manifest missing list: {key}", failures)

    for required in manifest.get("required_files", []):
        if isinstance(required, str):
            require((ROOT / required).is_file(), f"required file missing: {required}", failures)

    required_ids = {"PCD-FC-0", "PCD-FC-1", "PCD-FC-2", "PCD-FC-3", "PCD-MG-1", "PCD-MG-2"}
    actual_ids = set(manifest.get("claim_ids", []))
    require(required_ids.issubset(actual_ids), "manifest missing fixed-cutoff claim ids", failures)
    required_files = set(manifest.get("required_files", []))
    require(
        FORBIDDEN_PUBLIC_FILES.isdisjoint(required_files),
        "verification manifest includes files outside the public artifact surface",
        failures,
    )


def check_public_manifest_and_packet(failures: list[str]) -> None:
    """Check public manifest and packet docs."""
    for path in [PUBLIC_MANIFEST, PACKET]:
        require(path.is_file(), f"missing public file: {path.relative_to(ROOT)}", failures)
    manifest = load_json(PUBLIC_MANIFEST)
    require(isinstance(manifest, dict), "public manifest must be an object", failures)
    if isinstance(manifest, dict):
        required_files = set(manifest.get("required_files", []))
        exclusions = set(manifest.get("excluded_from_public_artifact", []))
        require(
            FORBIDDEN_PUBLIC_FILES.isdisjoint(required_files),
            "public manifest includes files outside the public artifact surface",
            failures,
        )
        require(
            "docs/ROADMAP.md" in exclusions and "internal verification records" in exclusions,
            "public manifest does not exclude roadmap/internal verification files",
            failures,
        )
    require_phrases(
        PACKET,
        [
            "PrimeClock Dynamics v0.2.0",
            "Fixed-Cutoff Foundation",
            "PCD-FC-0",
            "PCD-FC-1",
            "PCD-FC-2",
            "PCD-FC-3",
            "PCD-MG-1",
            "PCD-MG-2",
            "does not claim",
            "diagonal theorem",
        ],
        failures,
    )


def check_support_files(support_dir: Path, failures: list[str]) -> None:
    """Check deterministic support output schema and invariants."""
    for name in [
        "support_manifest.json",
        "crt_average_support.csv",
        "angular_moment_support.csv",
        "theorem0_support.json",
        "support_metadata.json",
    ]:
        require((support_dir / name).is_file(), f"missing support output: {name}", failures)

    support_manifest = load_json(support_dir / "support_manifest.json")
    require(isinstance(support_manifest, dict), "support manifest must be an object", failures)
    if isinstance(support_manifest, dict):
        require(support_manifest.get("artifact_id") == ARTIFACT_ID, "bad support artifact id", failures)
        require(support_manifest.get("crt_average_rows") == 4, "unexpected CRT support row count", failures)
        require(support_manifest.get("theorem0_checked_values") == 9999, "unexpected theorem0 count", failures)
        files = set(support_manifest.get("files", []))
        require("support_metadata.json" in files, "support metadata missing from support manifest", failures)

    theorem0 = load_json(support_dir / "theorem0_support.json")
    require(isinstance(theorem0, dict), "theorem0 support must be an object", failures)
    if isinstance(theorem0, dict):
        require(theorem0.get("all_match") is True, "theorem0 support did not match", failures)

    with (support_dir / "crt_average_support.csv").open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    require(len(rows) == 4, "CRT support CSV row count mismatch", failures)
    for row in rows:
        require(row.get("exact_average_equals_product") == "True", "CRT exact equality failed", failures)
        require(row.get("average_minus_baseline_fraction") == "0/1", "CRT support diff nonzero", failures)
        require(row.get("sample_count") == row.get("crt_period"), "CRT period/sample mismatch", failures)

    with (support_dir / "angular_moment_support.csv").open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    require(len(rows) == 9, "Angular support CSV row count mismatch", failures)
    require(all(row.get("exact_match") == "True" for row in rows), "Angular exact support failed", failures)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--support-dir", type=Path)
    args = parser.parse_args()

    failures: list[str] = []
    checks = [check_manifest, check_public_manifest_and_packet]
    for check in checks:
        check(failures)

    if args.support_dir is None:
        with tempfile.TemporaryDirectory(prefix="pcd-v0-2-support-") as tmp_dir:
            support_dir = Path(tmp_dir)
            build_support(support_dir)
            check_support_files(support_dir, failures)
    else:
        check_support_files(args.support_dir, failures)

    if failures:
        print("check_v0_2_public_artifact: failed")
        for failure in failures:
            print(f"FAIL: {failure}")
        raise SystemExit(1)
    print(f"check_v0_2_public_artifact: checks={len(checks) + 1}, failed=0")


if __name__ == "__main__":
    main()
