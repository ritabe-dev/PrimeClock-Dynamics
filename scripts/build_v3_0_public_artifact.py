#!/usr/bin/env python3
"""Build the focused v3.0.0 public artifact bundle."""

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
FROZEN_SOURCE_ROOT = ROOT / "artifacts/v3.0.0/source"
SOURCE_ROOT = FROZEN_SOURCE_ROOT if FROZEN_SOURCE_ROOT.is_dir() else ROOT
TOP_LEVEL = "PrimeClock-Dynamics-v3.0.0"
ZIP_NAME = f"{TOP_LEVEL}.zip"
ZIP_TIMESTAMP = (1980, 1, 1, 0, 0, 0)

INCLUDE_EXACT = {
    "LICENSE",
    "pyproject.toml",
    "setup.py",
    "README_V3_0_0_RELEASE.md",
    "RELEASE_NOTES_v3_0_0_PUBLIC.md",
    "CITATION_v3_0_0_RELEASE.cff",
    "ARTIFACT_MANIFEST_v3_0_0_PUBLIC.json",
    "docs/MB_V3_0_RELEASE_CLAIM_BOUNDARY.md",
    "docs/MB_V3_0_MATH_SPEC.md",
    "paper/primeclock_dynamics_v3_0_release_manuscript.md",
    "experiments/__init__.py",
    "experiments/mb/__init__.py",
    "experiments/mb/run_mb_v3_0_support.py",
    "experiments/mb/run_mb_v3_0_public_support.py",
    "experiments/_workflow/check_v3_0_public_artifact.py",
    "experiments/_workflow/README_V3_0_PUBLIC_ARTIFACT.md",
    "experiments/_workflow/pcd_v3_0_public_artifact.json",
    "scripts/build_v3_0_public_artifact.py",
    "scripts/check_text_hygiene.py",
    "scripts/verify_candidate_workflow.py",
    "tests/test_mertens_boundary.py",
    "tests/test_mb_v3_0_public_surface.py",
    "tests/test_text_hygiene.py",
}

SOURCE_ALIASES = {
    "README_V3_0_0_RELEASE.md": "README.md",
    "RELEASE_NOTES_v3_0_0_PUBLIC.md": "RELEASE_NOTES_v3_0_0.md",
    "CITATION_v3_0_0_RELEASE.cff": "CITATION.cff",
    "ARTIFACT_MANIFEST_v3_0_0_PUBLIC.json": "ARTIFACT_MANIFEST_v3_0_0.json",
    "docs/MB_V3_0_RELEASE_CLAIM_BOUNDARY.md": "docs/MB_V3_0_PUBLIC_CLAIM_BOUNDARY.md",
    "paper/primeclock_dynamics_v3_0_release_manuscript.md": "paper/primeclock_dynamics_v3_0_public_manuscript.md",
}

FORBIDDEN_MEMBERS = {
    "artifacts/",
    "docs/internal/",
    "app/",
    "data/",
    "support_evidence/akc_v2_0_public_support/",
    "gate_c_support/",
    "gate_p_support/",
    "paper/mertens_boundary_v3_0_gate_r.md",
    "paper/mertens_boundary_v3_0_gate_c.md",
    "experiments/mb/run_mb_v3_0_gate_r_support.py",
    "experiments/mb/run_mb_v3_0_gate_c_support.py",
    "experiments/_workflow/pcd_v3_0_mertens_boundary_gate_r.json",
    "experiments/_workflow/pcd_v3_0_mertens_boundary_gate_c.json",
    "experiments/_workflow/README_V3_0_GATE_R.md",
    "experiments/_workflow/README_V3_0_GATE_C.md",
    "scripts/build_v3_0_gate_r_review_zip.py",
    "scripts/build_v3_0_gate_c_candidate_bundle.py",
    "experiments/_workflow/V3_0_GATE_R_PASS.md",
    "experiments/_workflow/V3_0_GATE_C_PASS.md",
    "experiments/_workflow/README_V3_0_GATE_P.md",
    "experiments/_workflow/pcd_v3_0_mertens_boundary_gate_p.json",
    "experiments/_workflow/check_v3_0_gate_p_candidate.py",
    "scripts/build_v3_0_gate_p_candidate_bundle.py",
    "tests/test_mb_v3_0_gate_p_surface.py",
    "docs/MB_V3_0_GATE_C_CLAIM_BOUNDARY.md",
    "paper/primeclock_dynamics_v2_0_public_manuscript.md",
    "ARTIFACT_MANIFEST_v2_0_0.json",
    "RELEASE_NOTES_v2_0_0.md",
}


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def run_command(cwd: Path, command: list[str], *, env_overrides: dict[str, str] | None = None) -> None:
    env = os.environ.copy()
    env["PYTHONPATH"] = str(cwd / "src") + os.pathsep + str(cwd) + os.pathsep + env.get("PYTHONPATH", "")
    env.setdefault("RUFF_CACHE_DIR", "/tmp/pcd-ruff-cache")
    if env_overrides:
        env.update(env_overrides)
    completed = subprocess.run(command, cwd=cwd, env=env, text=True, check=False)
    if completed.returncode != 0:
        raise SystemExit("public artifact bundle verification failed: " + " ".join(command))


def source_files() -> list[Path]:
    files: list[Path] = []
    for relative in sorted(INCLUDE_EXACT):
        path = SOURCE_ROOT / relative
        if not path.is_file():
            alias = SOURCE_ALIASES.get(relative)
            if alias is not None and (SOURCE_ROOT / alias).is_file():
                path = SOURCE_ROOT / alias
            else:
                raise SystemExit(f"required v3.0 public artifact file missing: {relative}")
        files.append(path)
    for path in sorted((SOURCE_ROOT / "src/prime_clock_dynamics").glob("*.py")):
        files.append(path)
    return sorted(files, key=lambda item: archive_relative(item).as_posix())


def archive_relative(path: Path) -> Path:
    relative = path.relative_to(SOURCE_ROOT).as_posix()
    return Path(SOURCE_ALIASES.get(relative, relative))


def write_stable_file(archive: zipfile.ZipFile, source: Path, archive_name: Path) -> None:
    info = zipfile.ZipInfo(archive_name.as_posix(), date_time=ZIP_TIMESTAMP)
    info.compress_type = zipfile.ZIP_DEFLATED
    info.external_attr = 0o644 << 16
    archive.writestr(info, source.read_bytes())


def build_support(support_dir: Path) -> list[Path]:
    support_dir.mkdir(parents=True, exist_ok=True)
    run_command(
        SOURCE_ROOT,
        [
            sys.executable,
            "experiments/mb/run_mb_v3_0_public_support.py",
            "--out-dir",
                str(support_dir / "mb_v3_0_public_support"),
        ],
    )
    return sorted(path for path in support_dir.rglob("*") if path.is_file())


def verify_members(zip_path: Path) -> None:
    with zipfile.ZipFile(zip_path) as archive:
        names = archive.namelist()
    for marker in FORBIDDEN_MEMBERS:
        needle = f"{TOP_LEVEL}/{marker}"
        if any(name == needle or name.startswith(needle) or marker in name for name in names):
            raise SystemExit(f"v3.0 public artifact contains excluded marker: {marker}")
    required = {
        f"{TOP_LEVEL}/README.md",
        f"{TOP_LEVEL}/CITATION.cff",
        f"{TOP_LEVEL}/paper/primeclock_dynamics_v3_0_public_manuscript.md",
        f"{TOP_LEVEL}/docs/MB_V3_0_PUBLIC_CLAIM_BOUNDARY.md",
        f"{TOP_LEVEL}/support_evidence/mb_v3_0_public_support/summary.json",
    }
    missing = required.difference(names)
    if missing:
        raise SystemExit(f"v3.0 public artifact missing required members: {sorted(missing)}")


def verify_extraction(zip_path: Path) -> None:
    with tempfile.TemporaryDirectory(prefix="pcd-v3-0-gate-p-extract-") as tmp_dir:
        extract_root = Path(tmp_dir)
        with zipfile.ZipFile(zip_path) as archive:
            archive.extractall(extract_root)
        repo = extract_root / TOP_LEVEL
        if not repo.is_dir():
            raise SystemExit(f"extracted top-level directory missing: {repo}")
        run_command(repo, [sys.executable, "experiments/_workflow/check_v3_0_public_artifact.py"])
        run_command(
            repo,
            [
                sys.executable,
                "scripts/verify_candidate_workflow.py",
                "--config",
                "experiments/_workflow/pcd_v3_0_public_artifact.json",
                "quick",
            ],
        )
        run_command(
            repo,
            [
                sys.executable,
                "-m",
                "pytest",
                "tests/test_mertens_boundary.py",
                "tests/test_mb_v3_0_public_surface.py",
                "tests/test_text_hygiene.py",
                "-q",
            ],
            env_overrides={"PYTEST_DISABLE_PLUGIN_AUTOLOAD": "1"},
        )


def build_zip(out_dir: Path, *, verify: bool) -> tuple[Path, Path, int]:
    out_dir.mkdir(parents=True, exist_ok=True)
    zip_path = out_dir / ZIP_NAME
    sha_path = zip_path.with_suffix(".zip.sha256")

    with tempfile.TemporaryDirectory(prefix="pcd-v3-0-gate-p-support-") as tmp_dir:
        support_dir = Path(tmp_dir) / "support_evidence"
        support_files = build_support(support_dir)
        files = source_files()
        with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
            for path in files:
                write_stable_file(archive, path, Path(TOP_LEVEL) / archive_relative(path))
            for path in support_files:
                write_stable_file(
                    archive,
                    path,
                    Path(TOP_LEVEL) / "support_evidence" / path.relative_to(support_dir),
                )

    verify_members(zip_path)
    digest = sha256_file(zip_path)
    sha_path.write_text(f"{digest}  {zip_path.name}\n", encoding="utf-8")

    if verify:
        verify_extraction(zip_path)
        print("v3_0_public_artifact: verified_extraction=1")

    return zip_path, sha_path, len(source_files()) + len(support_files)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=Path, default=Path("/tmp"))
    parser.add_argument("--verify-extraction", action="store_true")
    args = parser.parse_args()

    zip_path, sha_path, file_count = build_zip(args.out, verify=args.verify_extraction)
    print(f"v3_0_public_artifact: zip={zip_path}")
    print(f"v3_0_public_artifact: sha256={sha_path}")
    print(f"v3_0_public_artifact: files={file_count}")


if __name__ == "__main__":
    main()
