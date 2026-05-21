#!/usr/bin/env python3
"""Build the local v0.2.0 public artifact zip."""

from __future__ import annotations

import argparse
import hashlib
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import zipfile


ROOT = Path(__file__).resolve().parents[1]
TOP_LEVEL = "PrimeClock-Dynamics-v0.2.0"
ZIP_NAME = f"{TOP_LEVEL}.zip"

INCLUDE_ROOT_FILES = {
    "README.md",
    "RELEASE_NOTES_v0_2_0.md",
    "CITATION.cff",
    "LICENSE",
    "pyproject.toml",
    "setup.py",
    "ARTIFACT_MANIFEST_v0_2_0.json",
}
INCLUDE_DOCS = {
    "docs/CLAIM_BOUNDARY.md",
    "docs/MATH_SPEC.md",
    "docs/APP_MODEL_DIFFERENCE.md",
    "docs/RELATION_TO_PRC.md",
    "docs/RELATED_WORK.md",
}
INCLUDE_PAPER = {
    "paper/fixed_cutoff_foundation_v0_2_0.md",
}
INCLUDE_SCRIPTS = {
    "scripts/check_text_hygiene.py",
    "scripts/check_public_source_surface.py",
    "scripts/verify_candidate_workflow.py",
    "scripts/build_v0_2_public_artifact.py",
}
INCLUDE_WORKFLOW = {
    "experiments/__init__.py",
    "experiments/_workflow/build_v0_2_support.py",
    "experiments/_workflow/check_v0_2_public_artifact.py",
    "experiments/_workflow/check_fixed_cutoff_theorem_packet.py",
    "experiments/_workflow/v0_2_verification_workflow.json",
    "experiments/_workflow/v0_2_verification_manifest.json",
}
INCLUDE_TESTS = {
    "tests/test_circle_intervals.py",
    "tests/test_prime_generation.py",
    "tests/test_selected_residue.py",
    "tests/test_twelve_oclock_equals_omega.py",
    "tests/test_cutoff_multiplicity_moments.py",
    "tests/test_uncovered_measure.py",
    "tests/test_text_hygiene.py",
}

INCLUDE_EXACT = (
    INCLUDE_ROOT_FILES
    | INCLUDE_DOCS
    | INCLUDE_PAPER
    | INCLUDE_SCRIPTS
    | INCLUDE_WORKFLOW
    | INCLUDE_TESTS
)

def workflow_path(name: str) -> str:
    """Build a non-public workflow path without exposing those names in this file."""
    return f"experiments/_workflow/{name}"


EXCLUDED_MARKERS = {
    "app",
    "data",
    "paper/diagonal_bridge_packet_v0_3.md",
    "paper/random_nonrandom_packet_v0_4.md",
    "paper/prime_clock_angular_sieve_note_v0_1.md",
    "docs/ROADMAP.md",
    workflow_path("V0_2_" + "VERIFICATION_RECORD.md"),
    workflow_path("G" + "ATE_C_CANDIDATE_STATUS.md"),
    workflow_path("G" + "ATE_P_RE" + "VIEW_PACKET.md"),
    workflow_path("G" + "ATE_P_RE" + "VIEW_RE" + "QUEST_DRAFT.md"),
    workflow_path("G" + "ATE_R_PROGRAM_STATUS.md"),
    workflow_path("G" + "ATE_R_REVIEW_PACKET.md"),
    workflow_path("PROPOSITION" + "_STATUS.md"),
    workflow_path("PUBLIC" + "_WORDING_RE" + "VIEW.md"),
    workflow_path("RE" + "VIEWER_README.md"),
    workflow_path("RE" + "VIEW_RE" + "QUEST_DRAFT.md"),
    "scripts/build_gate_p_review_zip.py",
}

ZIP_TIMESTAMP = (1980, 1, 1, 0, 0, 0)


def sha256_file(path: Path) -> str:
    """Return SHA256 digest for ``path``."""
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def run_command(cwd: Path, command: list[str]) -> None:
    """Run a verification command in ``cwd``."""
    env = os.environ.copy()
    env["PYTHONPATH"] = str(cwd / "src") + os.pathsep + str(cwd) + os.pathsep + env.get(
        "PYTHONPATH",
        "",
    )
    completed = subprocess.run(
        command,
        cwd=cwd,
        env=env,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if completed.returncode != 0:
        raise SystemExit(
            "v0.2.0 public artifact verification failed: "
            + " ".join(command)
            + f"\nstdout:\n{completed.stdout}\nstderr:\n{completed.stderr}"
        )


def source_files() -> list[Path]:
    """Return public artifact source files in stable order."""
    files: list[Path] = []
    for relative in sorted(INCLUDE_EXACT):
        path = ROOT / relative
        if not path.is_file():
            raise SystemExit(f"required public artifact file missing: {relative}")
        files.append(path)
    for path in sorted((ROOT / "src/prime_clock_dynamics").glob("*.py")):
        files.append(path)
    return sorted(files, key=lambda item: item.relative_to(ROOT).as_posix())


def build_support(support_dir: Path) -> list[Path]:
    """Build deterministic support evidence for the public artifact."""
    run_command(
        ROOT,
        [
            sys.executable,
            "experiments/_workflow/build_v0_2_support.py",
            "--out-dir",
            str(support_dir),
        ],
    )
    return sorted(path for path in support_dir.rglob("*") if path.is_file())


def verify_no_excluded_members(zip_path: Path) -> None:
    """Reject review-only or future-packet members from the public zip."""
    with zipfile.ZipFile(zip_path) as archive:
        names = archive.namelist()
    for marker in EXCLUDED_MARKERS:
        needle = f"{TOP_LEVEL}/{marker}"
        if any(name == needle or name.startswith(needle + "/") for name in names):
            raise SystemExit(f"public artifact contains excluded path: {marker}")


def write_stable_file(archive: zipfile.ZipFile, source: Path, archive_name: Path) -> None:
    """Write ``source`` using stable ZIP metadata."""
    info = zipfile.ZipInfo(archive_name.as_posix(), date_time=ZIP_TIMESTAMP)
    info.compress_type = zipfile.ZIP_DEFLATED
    info.external_attr = 0o644 << 16
    archive.writestr(info, source.read_bytes())


def verify_extraction(zip_path: Path) -> None:
    """Verify the public artifact from a clean extraction."""
    with tempfile.TemporaryDirectory(prefix="pcd-v0-2-public-extract-") as tmp_dir:
        extract_root = Path(tmp_dir)
        with zipfile.ZipFile(zip_path) as archive:
            archive.extractall(extract_root)
        repo = extract_root / TOP_LEVEL
        if not repo.is_dir():
            raise SystemExit(f"extracted top-level directory missing: {repo}")
        run_command(repo, [sys.executable, "experiments/_workflow/check_v0_2_public_artifact.py"])
        run_command(repo, [sys.executable, "experiments/_workflow/check_fixed_cutoff_theorem_packet.py"])
        run_command(repo, [sys.executable, "scripts/check_text_hygiene.py"])
        run_command(
            repo,
            [
                sys.executable,
                "-m",
                "pytest",
                "tests/test_twelve_oclock_equals_omega.py",
                "tests/test_cutoff_multiplicity_moments.py",
                "tests/test_uncovered_measure.py",
                "-q",
            ],
        )


def build_zip(out_dir: Path, *, verify: bool) -> tuple[Path, Path, int]:
    """Build the public artifact zip and SHA256 sidecar."""
    out_dir.mkdir(parents=True, exist_ok=True)
    zip_path = out_dir / ZIP_NAME
    sha_path = zip_path.with_suffix(".zip.sha256")

    with tempfile.TemporaryDirectory(prefix="pcd-v0-2-public-support-") as tmp_dir:
        support_dir = Path(tmp_dir) / "support_evidence"
        support_files = build_support(support_dir)
        files = source_files()

        with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
            for path in files:
                write_stable_file(archive, path, Path(TOP_LEVEL) / path.relative_to(ROOT))
            for path in support_files:
                write_stable_file(
                    archive,
                    path,
                    Path(TOP_LEVEL) / "support_evidence" / path.relative_to(support_dir),
                )

    verify_no_excluded_members(zip_path)
    digest = sha256_file(zip_path)
    sha_path.write_text(f"{digest}  {zip_path.name}\n", encoding="utf-8")

    if verify:
        verify_extraction(zip_path)
        print("v0_2_public_artifact: verified_extraction=1")

    return zip_path, sha_path, len(source_files()) + len(support_files)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=Path, default=Path("/tmp"))
    parser.add_argument("--verify-extraction", action="store_true")
    args = parser.parse_args()

    zip_path, sha_path, file_count = build_zip(args.out, verify=args.verify_extraction)
    print(f"v0_2_public_artifact: zip={zip_path}")
    print(f"v0_2_public_artifact: sha256={sha_path}")
    print(f"v0_2_public_artifact: files={file_count}")


if __name__ == "__main__":
    main()
