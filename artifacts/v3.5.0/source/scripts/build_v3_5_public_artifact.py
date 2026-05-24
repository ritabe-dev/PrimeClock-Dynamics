#!/usr/bin/env python3
"""Build the v3.5.0 integer-time transfer public artifact."""

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
FROZEN_SOURCE_ROOT = ROOT / "artifacts/v3.5.0/source"
SOURCE_ROOT = FROZEN_SOURCE_ROOT if FROZEN_SOURCE_ROOT.is_dir() else ROOT
TOP_LEVEL = "PrimeClock-Dynamics-v3.5.0"
ZIP_NAME = f"{TOP_LEVEL}.zip"
ZIP_TIMESTAMP = (1980, 1, 1, 0, 0, 0)

INCLUDE_EXACT = {
    "LICENSE",
    "README.md",
    "RELEASE_NOTES_v3_5_0.md",
    "CITATION.cff",
    "ARTIFACT_MANIFEST_v3_5_0.json",
    "pyproject.toml",
    "setup.py",
    "docs/IT_V3_5_PUBLIC_CLAIM_BOUNDARY.md",
    "paper/primeclock_dynamics_v3_5_public_manuscript.md",
    "experiments/__init__.py",
    "experiments/_workflow/README_V3_5_PUBLIC_ARTIFACT.md",
    "experiments/_workflow/pcd_v3_5_public_artifact.json",
    "experiments/it/__init__.py",
    "experiments/it/run_v3_5_public_support.py",
    "experiments/it/_workflow/check_v3_5_public_artifact.py",
    "scripts/build_v3_5_public_artifact.py",
    "scripts/check_text_hygiene.py",
    "scripts/verify_candidate_workflow.py",
    "tests/test_integer_time_transfer.py",
    "tests/test_it_v3_5_public_surface.py",
    "tests/test_text_hygiene.py",
}

SOURCE_ALIASES = {
    "README.md": "README_V3_5_0_PUBLIC.md",
    "CITATION.cff": "CITATION_v3_5_0_PUBLIC.cff",
}

FORBIDDEN_MEMBERS = {
    "docs/internal/",
    "artifacts/",
    "app/",
    "data/",
    "AKC_PROGRAM.md",
    "AKC_VERSION_SURFACE_MAP.md",
    "gate_" + "c_support/",
    "gate_" + "p_support/",
    "docs/IT_V3_5_GATE_C",
    "docs/IT_V3_5_GATE_P",
    "integer_time_transfer_v3_5_gate_c",
    "integer_time_transfer_v3_5_gate_p",
    "run_v3_5_gate_" + "c_support.py",
    "run_v3_5_gate_" + "p_support.py",
    "check_it_v3_5_gate_c.py",
    "check_it_v3_5_gate_p.py",
    "build_v3_5_gate_" + "c_candidate_bundle.py",
    "build_v3_5_gate_" + "p_candidate_bundle.py",
    "test_it_v3_5_gate_" + "c_surface.py",
    "test_it_v3_5_gate_" + "p_surface.py",
    "v2_0_public",
    "v3_0_public",
}


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def run_command(
    cwd: Path,
    command: list[str],
    *,
    env_overrides: dict[str, str] | None = None,
) -> None:
    env = os.environ.copy()
    env["PYTHONPATH"] = str(cwd / "src") + os.pathsep + str(cwd) + os.pathsep + env.get("PYTHONPATH", "")
    env.setdefault("RUFF_CACHE_DIR", "/tmp/pcd-dynamics-ruff-cache")
    if env_overrides:
        env.update(env_overrides)
    completed = subprocess.run(command, cwd=cwd, env=env, text=True, check=False)
    if completed.returncode != 0:
        raise SystemExit("v3.5 public artifact verification failed: " + " ".join(command))


def resolve_source(relative: str) -> Path:
    alias = SOURCE_ALIASES.get(relative)
    if alias is not None and (SOURCE_ROOT / alias).is_file():
        return SOURCE_ROOT / alias
    return SOURCE_ROOT / relative


def source_files() -> list[Path]:
    files: list[Path] = []
    for relative in sorted(INCLUDE_EXACT):
        path = resolve_source(relative)
        if not path.is_file():
            raise SystemExit(f"required v3.5 public artifact file missing: {relative}")
        files.append(path)
    for path in sorted((SOURCE_ROOT / "src/prime_clock_dynamics").glob("*.py")):
        files.append(path)
    return sorted(files, key=lambda item: archive_relative(item).as_posix())


def archive_relative(path: Path) -> Path:
    relative = path.relative_to(SOURCE_ROOT).as_posix()
    for archive_name, source_name in SOURCE_ALIASES.items():
        if relative == source_name:
            return Path(archive_name)
    return Path(relative)


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
            "experiments/it/run_v3_5_public_support.py",
            "--out-dir",
            str(support_dir / "support_evidence/it_v3_5_public_support"),
        ],
    )
    return sorted(path for path in support_dir.rglob("*") if path.is_file())


def verify_members(zip_path: Path) -> None:
    with zipfile.ZipFile(zip_path) as archive:
        names = archive.namelist()
    for marker in FORBIDDEN_MEMBERS:
        needle = f"{TOP_LEVEL}/{marker}"
        if any(name == needle or name.startswith(needle) or marker in name for name in names):
            raise SystemExit(f"v3.5 public artifact contains forbidden marker: {marker}")
    missing = {f"{TOP_LEVEL}/README.md", f"{TOP_LEVEL}/CITATION.cff"}.difference(names)
    if missing:
        raise SystemExit(f"v3.5 public artifact missing required aliases: {sorted(missing)}")


def verify_extraction(zip_path: Path) -> None:
    with tempfile.TemporaryDirectory(prefix="pcd-v3-5-public-extract-") as tmp_dir:
        extract_root = Path(tmp_dir)
        with zipfile.ZipFile(zip_path) as archive:
            archive.extractall(extract_root)
        repo = extract_root / TOP_LEVEL
        if not repo.is_dir():
            raise SystemExit(f"extracted top-level directory missing: {repo}")
        run_command(repo, [sys.executable, "experiments/it/_workflow/check_v3_5_public_artifact.py"])
        run_command(
            repo,
            [
                sys.executable,
                "scripts/check_text_hygiene.py",
                "--path",
                "docs/IT_V3_5_PUBLIC_CLAIM_BOUNDARY.md",
                "--path",
                "paper/primeclock_dynamics_v3_5_public_manuscript.md",
            ],
        )
        run_command(
            repo,
            [
                sys.executable,
                "-m",
                "pytest",
                "tests/test_integer_time_transfer.py",
                "tests/test_it_v3_5_public_surface.py",
                "tests/test_text_hygiene.py",
                "-q",
            ],
            env_overrides={"PYTEST_DISABLE_PLUGIN_AUTOLOAD": "1"},
        )


def build_zip(out_dir: Path, *, verify: bool) -> tuple[Path, Path, int]:
    out_dir.mkdir(parents=True, exist_ok=True)
    zip_path = out_dir / ZIP_NAME
    sha_path = zip_path.with_suffix(".zip.sha256")

    with tempfile.TemporaryDirectory(prefix="pcd-v3-5-public-support-") as tmp_dir:
        support_dir = Path(tmp_dir)
        support_files = build_support(support_dir)
        files = source_files()
        with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
            for path in files:
                write_stable_file(archive, path, Path(TOP_LEVEL) / archive_relative(path))
            for path in support_files:
                write_stable_file(archive, path, Path(TOP_LEVEL) / path.relative_to(support_dir))

    verify_members(zip_path)
    digest = sha256_file(zip_path)
    sha_path.write_text(f"{digest}  {zip_path.name}\n", encoding="utf-8")

    if verify:
        verify_extraction(zip_path)
        print("v3_5_public_artifact: verified_extraction=1")

    return zip_path, sha_path, len(source_files()) + len(support_files)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=Path, default=Path("/tmp"))
    parser.add_argument("--verify-extraction", action="store_true")
    args = parser.parse_args()

    zip_path, sha_path, file_count = build_zip(args.out, verify=args.verify_extraction)
    print(f"v3_5_public_artifact: zip={zip_path}")
    print(f"v3_5_public_artifact: sha256={sha_path}")
    print(f"v3_5_public_artifact: files={file_count}")


if __name__ == "__main__":
    main()
