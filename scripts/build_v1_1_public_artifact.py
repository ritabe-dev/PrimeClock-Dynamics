#!/usr/bin/env python3
"""Build the v1.1 public artifact."""

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
TOP_LEVEL = "PrimeClock-Dynamics-v1.1.0"
ZIP_NAME = f"{TOP_LEVEL}.zip"
ZIP_TIMESTAMP = (1980, 1, 1, 0, 0, 0)

INCLUDE_EXACT = {
    "README.md",
    "RELEASE_NOTES_v1_1_0.md",
    "CITATION.cff",
    "LICENSE",
    "pyproject.toml",
    "setup.py",
    "ARTIFACT_MANIFEST_v1_1_0.json",
    "docs/SAGF_CLAIM_BOUNDARY.md",
    "docs/SAGF_MATH_SPEC.md",
    "docs/SAGF_RELATED_WORK.md",
    "paper/primeclock_dynamics_v1_1_manuscript.md",
    "experiments/__init__.py",
    "experiments/akc/__init__.py",
    "experiments/akc/run_collision_kernel_by_scale.py",
    "experiments/_workflow/README_V1_1_PUBLIC_ARTIFACT.md",
    "experiments/_workflow/check_v1_1_public_artifact.py",
    "experiments/_workflow/pcd_v1_1_public_artifact.json",
    "experiments/_workflow/pcd_v1_1_public_artifact_manifest.json",
    "scripts/build_v1_1_public_artifact.py",
    "scripts/check_text_hygiene.py",
    "scripts/verify_candidate_workflow.py",
    "tests/test_collision_kernel.py",
}

SOURCE_ALIASES = {
    "README.md": "README_V1_1_0_PUBLIC.md",
    "RELEASE_NOTES_v1_1_0.md": "RELEASE_NOTES_v1_1_0_PUBLIC.md",
    "CITATION.cff": "CITATION_v1_1_0_PUBLIC.cff",
    "ARTIFACT_MANIFEST_v1_1_0.json": "ARTIFACT_MANIFEST_v1_1_0_PUBLIC.json",
}

FORBIDDEN_MEMBERS = {
    "docs/internal/",
    "app/",
    "data/",
    "artifacts/",
    "README_V1_1_0.md",
    "README_V1_1_0_PUBLIC.md",
    "CITATION_v1_1_0.cff",
    "CITATION_v1_1_0_PUBLIC.cff",
    "RELEASE_NOTES_v1_1_0_PUBLIC.md",
    "ARTIFACT_MANIFEST_v1_1_0_PUBLIC.json",
    "paper/primeclock_dynamics_v1_1_preprint.md",
    "paper/shrinking_angle_gaussian_field_v1_1_gate_c.md",
    "paper/angular_kubilius_chaos_v2_0_gate_r.md",
    "experiments/_workflow/V1_1_GATE_P_" + "CANDIDATE_STATUS.md",
    "experiments/_workflow/V1_1_GATE_C_STATUS.md",
    "experiments/_workflow/V1_1_GATE_R_REVIEW_PACKET.md",
    "experiments/_workflow/V1_1_GATE_R_REVIEW_REQUEST_DRAFT.md",
    "experiments/_workflow/README_V1_1_GATE_P.md",
    "experiments/_workflow/README_V1_1_GATE_C.md",
    "experiments/_workflow/README_V1_1_GATE_R.md",
}


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def run_command(cwd: Path, command: list[str]) -> None:
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
            "v1.1 public artifact verification failed: "
            + " ".join(command)
            + f"\nstdout:\n{completed.stdout}\nstderr:\n{completed.stderr}"
        )


def source_files() -> list[Path]:
    files: list[Path] = []
    for relative in sorted(INCLUDE_EXACT):
        if relative in SOURCE_ALIASES and (ROOT / SOURCE_ALIASES[relative]).is_file():
            path = ROOT / SOURCE_ALIASES[relative]
        else:
            path = ROOT / relative
        if not path.is_file():
            raise SystemExit(f"required v1.1 public artifact file missing: {relative}")
        files.append(path)
    for path in sorted((ROOT / "src/prime_clock_dynamics").glob("*.py")):
        files.append(path)
    return sorted(files, key=lambda item: item.relative_to(ROOT).as_posix())


def archive_relative(path: Path) -> Path:
    relative = path.relative_to(ROOT).as_posix()
    for archive_name, source_name in SOURCE_ALIASES.items():
        if relative == source_name:
            return Path(archive_name)
    return Path(relative)


def write_stable_file(archive: zipfile.ZipFile, source: Path, archive_name: Path) -> None:
    info = zipfile.ZipInfo(archive_name.as_posix(), date_time=ZIP_TIMESTAMP)
    info.compress_type = zipfile.ZIP_DEFLATED
    info.external_attr = 0o644 << 16
    archive.writestr(info, source.read_bytes())


def verify_members(zip_path: Path) -> None:
    with zipfile.ZipFile(zip_path) as archive:
        names = archive.namelist()
    for marker in FORBIDDEN_MEMBERS:
        needle = f"{TOP_LEVEL}/{marker}"
        if any(name == needle or name.startswith(needle) for name in names):
            raise SystemExit(f"v1.1 public artifact contains excluded path: {marker}")
    for required in [f"{TOP_LEVEL}/README.md", f"{TOP_LEVEL}/CITATION.cff"]:
        if required not in names:
            raise SystemExit(f"v1.1 public artifact missing required member: {required}")


def verify_extraction(zip_path: Path) -> None:
    with tempfile.TemporaryDirectory(prefix="pcd-v1-1-public-extract-") as tmp_dir:
        extract_root = Path(tmp_dir)
        with zipfile.ZipFile(zip_path) as archive:
            archive.extractall(extract_root)
        repo = extract_root / TOP_LEVEL
        if not repo.is_dir():
            raise SystemExit(f"extracted top-level directory missing: {repo}")
        run_command(repo, [sys.executable, "experiments/_workflow/check_v1_1_public_artifact.py"])
        run_command(repo, [sys.executable, "scripts/check_text_hygiene.py"])
        run_command(
            repo,
            [
                sys.executable,
                "scripts/verify_candidate_workflow.py",
                "--config",
                "experiments/_workflow/pcd_v1_1_public_artifact.json",
                "quick",
            ],
        )


def build_zip(out_dir: Path, *, verify: bool) -> tuple[Path, Path, int]:
    out_dir.mkdir(parents=True, exist_ok=True)
    zip_path = out_dir / ZIP_NAME
    sha_path = zip_path.with_suffix(".zip.sha256")

    files = source_files()
    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for path in files:
            write_stable_file(archive, path, Path(TOP_LEVEL) / archive_relative(path))

    verify_members(zip_path)
    digest = sha256_file(zip_path)
    sha_path.write_text(f"{digest}  {zip_path.name}\n", encoding="utf-8")

    if verify:
        verify_extraction(zip_path)
        print("v1_1_public_artifact: verified_extraction=1")

    return zip_path, sha_path, len(files)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=Path, default=Path("/tmp"))
    parser.add_argument("--verify-extraction", action="store_true")
    args = parser.parse_args()

    zip_path, sha_path, file_count = build_zip(args.out, verify=args.verify_extraction)
    print(f"v1_1_public_artifact: zip={zip_path}")
    print(f"v1_1_public_artifact: sha256={sha_path}")
    print(f"v1_1_public_artifact: files={file_count}")


if __name__ == "__main__":
    main()
