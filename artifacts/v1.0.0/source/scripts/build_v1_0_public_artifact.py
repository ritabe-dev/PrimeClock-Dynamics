#!/usr/bin/env python3
"""Build a v1.0 public artifact."""

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
FROZEN_SOURCE_ROOT = ROOT / "artifacts/v1.0.0/source"
SOURCE_ROOT = FROZEN_SOURCE_ROOT if FROZEN_SOURCE_ROOT.is_dir() else ROOT
TOP_LEVEL = "PrimeClock-Dynamics-v1.0.0"
ZIP_NAME = f"{TOP_LEVEL}.zip"
ZIP_TIMESTAMP = (1980, 1, 1, 0, 0, 0)

INCLUDE_EXACT = {
    "README.md",
    "RELEASE_NOTES_v1_0_0.md",
    "CITATION.cff",
    "LICENSE",
    "pyproject.toml",
    "setup.py",
    "ARTIFACT_MANIFEST_v1_0_0.json",
    "docs/CLAIM_BOUNDARY.md",
    "docs/MATH_SPEC.md",
    "docs/APP_MODEL_DIFFERENCE.md",
    "docs/RELATION_TO_PRC.md",
    "docs/RELATED_WORK.md",
    "paper/primeclock_dynamics_v1_0_preprint.md",
    "paper/fixed_cutoff_foundation_v0_2_0.md",
    "paper/fixed_cutoff_angular_clt_v0_5.md",
    "paper/truncated_angular_clt_v0_6.md",
    "paper/diagonal_tail_removal_v0_7.md",
    "paper/diagonal_angular_erdos_kac_v0_8.md",
    "paper/finite_dimensional_angular_ek_v0_9.md",
    "experiments/__init__.py",
    "experiments/_workflow/README_V1_0_PUBLIC_ARTIFACT.md",
    "experiments/_workflow/check_v1_0_public_artifact.py",
    "experiments/_workflow/check_truncated_angular_clt_packet.py",
    "experiments/_workflow/check_diagonal_tail_removal_packet.py",
    "experiments/_workflow/check_diagonal_angular_ek_packet.py",
    "experiments/_workflow/check_finite_dimensional_angular_ek_packet.py",
    "experiments/_workflow/build_truncated_angular_clt_support.py",
    "experiments/_workflow/build_diagonal_tail_support.py",
    "experiments/_workflow/build_diagonal_angular_ek_support.py",
    "experiments/_workflow/build_finite_dimensional_angular_ek_support.py",
    "experiments/_workflow/pcd_v1_0_public_artifact.json",
    "experiments/_workflow/pcd_v1_0_public_artifact_manifest.json",
    "scripts/build_v1_0_public_artifact.py",
    "scripts/check_text_hygiene.py",
    "scripts/verify_candidate_workflow.py",
    "tests/test_text_hygiene.py",
    "tests/test_truncated_angular_clt_support.py",
    "tests/test_diagonal_tail_support.py",
    "tests/test_diagonal_angular_ek_support.py",
    "tests/test_finite_dimensional_angular_ek_support.py",
}

FORBIDDEN_MEMBERS = {
    "docs/ROADMAP.md",
    "docs/internal/",
    "app/",
    "data/",
    "artifacts/",
    "paper/integrated_angular_ek_mertens_v1_0.md",
    "paper/diagonal_bridge_packet_v0_3.md",
    "paper/random_nonrandom_packet_v0_4.md",
    "experiments/_workflow/GATE_R_PROGRAM_STATUS.md",
    "experiments/_workflow/PROPOSITION_STATUS.md",
    "experiments/_workflow/V1_0_GATE_C_PASS_RECORD.md",
    "experiments/_workflow/V1_0_GATE_C_CANDIDATE_STATUS.md",
}


def sha256_file(path: Path) -> str:
    """Return SHA256 digest for ``path``."""
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def run_command(cwd: Path, command: list[str]) -> None:
    """Run a verification command with local package paths."""
    env = os.environ.copy()
    env["PYTHONPATH"] = str(cwd / "src") + os.pathsep + str(cwd) + os.pathsep + env.get("PYTHONPATH", "")
    env.setdefault("RUFF_CACHE_DIR", "/tmp/pcd-ruff-cache")
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
            "v1.0 public artifact bundle verification failed: "
            + " ".join(command)
            + f"\nstdout:\n{completed.stdout}\nstderr:\n{completed.stderr}"
        )


def source_root() -> Path:
    """Return the frozen v1.0.0 public artifact source root."""
    return SOURCE_ROOT


def source_files() -> list[Path]:
    """Return public artifact source files in stable order."""
    source_root()
    files: list[Path] = []
    for relative in sorted(INCLUDE_EXACT):
        path = SOURCE_ROOT / relative
        if not path.is_file():
            raise SystemExit(f"required v1.0 Gate P file missing: {relative}")
        files.append(path)
    for path in sorted((SOURCE_ROOT / "src/prime_clock_dynamics").glob("*.py")):
        files.append(path)
    return sorted(files, key=lambda item: item.relative_to(SOURCE_ROOT).as_posix())


def write_stable_file(archive: zipfile.ZipFile, source: Path, archive_name: Path) -> None:
    """Write ``source`` using stable ZIP metadata."""
    info = zipfile.ZipInfo(archive_name.as_posix(), date_time=ZIP_TIMESTAMP)
    info.compress_type = zipfile.ZIP_DEFLATED
    info.external_attr = 0o644 << 16
    archive.writestr(info, source.read_bytes())


def verify_members(zip_path: Path) -> None:
    """Reject internal, diagnostic, or generated members."""
    with zipfile.ZipFile(zip_path) as archive:
        names = archive.namelist()
    for marker in FORBIDDEN_MEMBERS:
        needle = f"{TOP_LEVEL}/{marker}"
        if any(name == needle or name.startswith(needle) for name in names):
            raise SystemExit(f"v1.0 public artifact contains excluded path: {marker}")


def verify_extraction(zip_path: Path) -> None:
    """Verify the public artifact from a clean extraction."""
    with tempfile.TemporaryDirectory(prefix="pcd-v1-0-gate-p-extract-") as tmp_dir:
        extract_root = Path(tmp_dir)
        with zipfile.ZipFile(zip_path) as archive:
            archive.extractall(extract_root)
        repo = extract_root / TOP_LEVEL
        if not repo.is_dir():
            raise SystemExit(f"extracted top-level directory missing: {repo}")
        run_command(repo, [sys.executable, "experiments/_workflow/check_v1_0_public_artifact.py"])
        run_command(repo, [sys.executable, "scripts/check_text_hygiene.py"])
        run_command(
            repo,
            [
                sys.executable,
                "scripts/verify_candidate_workflow.py",
                "--config",
                "experiments/_workflow/pcd_v1_0_public_artifact.json",
                "quick",
            ],
        )


def build_zip(out_dir: Path, *, verify: bool) -> tuple[Path, Path, int]:
    """Build the public artifact zip and SHA256 sidecar."""
    out_dir.mkdir(parents=True, exist_ok=True)
    zip_path = out_dir / ZIP_NAME
    sha_path = zip_path.with_suffix(".zip.sha256")

    files = source_files()
    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for path in files:
            write_stable_file(archive, path, Path(TOP_LEVEL) / path.relative_to(SOURCE_ROOT))

    verify_members(zip_path)
    digest = sha256_file(zip_path)
    sha_path.write_text(f"{digest}  {zip_path.name}\n", encoding="utf-8")

    if verify:
        verify_extraction(zip_path)
        print("v1_0_public_artifact: verified_extraction=1")

    return zip_path, sha_path, len(files)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=Path, default=Path("/tmp"))
    parser.add_argument("--verify-extraction", action="store_true")
    args = parser.parse_args()

    zip_path, sha_path, file_count = build_zip(args.out, verify=args.verify_extraction)
    print(f"v1_0_public_artifact: zip={zip_path}")
    print(f"v1_0_public_artifact: sha256={sha_path}")
    print(f"v1_0_public_artifact: files={file_count}")


if __name__ == "__main__":
    main()
