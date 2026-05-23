#!/usr/bin/env python3
"""Build the focused v2.0.0 public artifact bundle."""

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
TOP_LEVEL = "PrimeClock-Dynamics-v2.0.0"
ZIP_NAME = f"{TOP_LEVEL}.zip"
ZIP_TIMESTAMP = (1980, 1, 1, 0, 0, 0)

INCLUDE_EXACT = {
    "README.md",
    "RELEASE_NOTES_v2_0_0.md",
    "CITATION.cff",
    "LICENSE",
    "pyproject.toml",
    "setup.py",
    "ARTIFACT_MANIFEST_v2_0_0.json",
    "docs/AKC_V2_0_PUBLIC_CLAIM_BOUNDARY.md",
    "paper/primeclock_dynamics_v2_0_public_manuscript.md",
    "experiments/__init__.py",
    "experiments/akc/__init__.py",
    "experiments/akc/run_akc_v2_0_support_experiments.py",
    "experiments/akc/run_akc_v2_0_public_support.py",
    "experiments/_workflow/README_V2_0_PUBLIC_ARTIFACT.md",
    "experiments/_workflow/check_v2_0_public_artifact.py",
    "experiments/_workflow/pcd_v2_0_public_artifact.json",
    "experiments/_workflow/pcd_v2_0_public_artifact_manifest.json",
    "scripts/build_v2_0_public_artifact.py",
    "scripts/check_text_hygiene.py",
    "scripts/verify_candidate_workflow.py",
    "tests/test_akc.py",
    "tests/test_akc_v2_0_public_surface.py",
    "tests/test_text_hygiene.py",
}

SOURCE_ALIASES = {
    "README.md": "README_V2_0_0_PUBLIC.md",
    "CITATION.cff": "CITATION_v2_0_0_PUBLIC.cff",
    "RELEASE_NOTES_v2_0_0.md": "RELEASE_NOTES_v2_0_0_PUBLIC.md",
    "ARTIFACT_MANIFEST_v2_0_0.json": "ARTIFACT_MANIFEST_v2_0_0_PUBLIC.json",
}

FORBIDDEN_MEMBERS = {
    "docs/internal/",
    "app/",
    "data/",
    "artifacts/",
    "paper/angular_kubilius_chaos_v2_0_gate_" + "c.md",
    "paper/angular_kubilius_chaos_v2_0_gate_" + "r.md",
    "experiments/_workflow/README_V2_0_GATE_C.md",
    "experiments/_workflow/README_V2_0_GATE_R.md",
    "experiments/_workflow/README_V2_0_GATE_" + "P.md",
    "experiments/_workflow/V2_0_GATE_C_STATUS.md",
    "experiments/_workflow/V2_0_GATE_" + "P_CANDIDATE_STATUS.md",
    "experiments/_workflow/pcd_v2_0_akc_gate_" + "c.json",
    "experiments/_workflow/pcd_v2_0_akc_gate_" + "r.json",
    "experiments/_workflow/pcd_v2_0_akc_gate_" + "p.json",
    "experiments/akc/_workflow/check_akc_v2_0_gate_" + "c.py",
    "experiments/akc/_workflow/check_akc_v2_0_gate_" + "r.py",
    "experiments/_workflow/check_v2_0_gate_" + "p_candidate.py",
    "experiments/akc/run_akc_v2_0_gate_" + "c_support.py",
    "experiments/akc/run_akc_v2_0_gate_" + "p_support.py",
    "experiments/akc/run_akc_v2_0_gate_" + "r_experiments.py",
    "scripts/build_v2_0_akc_gate_" + "c_candidate_bundle.py",
    "scripts/build_v2_0_akc_gate_" + "r_review_zip.py",
    "scripts/build_v2_0_gate_" + "p_candidate_bundle.py",
    "tests/test_akc_v2_0_gate_" + "c_surface.py",
    "tests/test_akc_v2_0_gate_" + "p_surface.py",
    "tests/test_akc_v2_0_gate_" + "r.py",
    "phase0",
    "prime_time_trace",
    "high_points_workstream",
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
    completed = subprocess.run(
        command,
        cwd=cwd,
        env=env,
        text=True,
        check=False,
    )
    if completed.returncode != 0:
        raise SystemExit(
            "v2.0 public artifact bundle verification failed: "
            + " ".join(command)
        )


def resolve_source(relative: str) -> Path:
    alias = SOURCE_ALIASES.get(relative)
    if alias is not None and (ROOT / alias).is_file():
        return ROOT / alias
    return ROOT / relative


def source_files() -> list[Path]:
    files: list[Path] = []
    for relative in sorted(INCLUDE_EXACT):
        path = resolve_source(relative)
        if not path.is_file():
            raise SystemExit(f"required v2.0 public artifact file missing: {relative}")
        files.append(path)
    for path in sorted((ROOT / "src/prime_clock_dynamics").glob("*.py")):
        files.append(path)
    return sorted(files, key=lambda item: archive_relative(item).as_posix())


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


def build_support(support_dir: Path) -> list[Path]:
    support_dir.mkdir(parents=True, exist_ok=True)
    run_command(
        ROOT,
        [
            sys.executable,
            "experiments/akc/run_akc_v2_0_public_support.py",
            "--out-dir",
            str(support_dir / "akc_v2_0_public_support"),
        ],
    )
    return sorted(path for path in support_dir.rglob("*") if path.is_file())


def verify_members(zip_path: Path) -> None:
    with zipfile.ZipFile(zip_path) as archive:
        names = archive.namelist()
    for marker in FORBIDDEN_MEMBERS:
        needle = f"{TOP_LEVEL}/{marker}"
        if any(name == needle or name.startswith(needle) or marker in name for name in names):
            raise SystemExit(f"v2.0 public artifact contains excluded marker: {marker}")
    required_aliases = {f"{TOP_LEVEL}/README.md", f"{TOP_LEVEL}/CITATION.cff"}
    missing = required_aliases.difference(names)
    if missing:
        raise SystemExit(f"v2.0 public artifact missing aliases: {sorted(missing)}")


def verify_extraction(zip_path: Path) -> None:
    with tempfile.TemporaryDirectory(prefix="pcd-v2-0-gate-p-extract-") as tmp_dir:
        extract_root = Path(tmp_dir)
        with zipfile.ZipFile(zip_path) as archive:
            archive.extractall(extract_root)
        repo = extract_root / TOP_LEVEL
        if not repo.is_dir():
            raise SystemExit(f"extracted top-level directory missing: {repo}")
        run_command(repo, [sys.executable, "experiments/_workflow/check_v2_0_public_artifact.py"])
        run_command(repo, [sys.executable, "scripts/check_text_hygiene.py"])
        run_command(
            repo,
            [
                sys.executable,
                "-m",
                "pytest",
                "tests/test_akc.py",
                "tests/test_akc_v2_0_public_surface.py",
                "tests/test_text_hygiene.py",
                "-q",
            ],
            env_overrides={"PYTEST_DISABLE_PLUGIN_AUTOLOAD": "1"},
        )


def build_zip(out_dir: Path, *, verify: bool) -> tuple[Path, Path, int]:
    out_dir.mkdir(parents=True, exist_ok=True)
    zip_path = out_dir / ZIP_NAME
    sha_path = zip_path.with_suffix(".zip.sha256")

    with tempfile.TemporaryDirectory(prefix="pcd-v2-0-gate-p-support-") as tmp_dir:
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
        print("v2_0_public_artifact: verified_extraction=1")

    return zip_path, sha_path, len(source_files()) + len(support_files)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=Path, default=Path("/tmp"))
    parser.add_argument("--verify-extraction", action="store_true")
    args = parser.parse_args()

    zip_path, sha_path, file_count = build_zip(args.out, verify=args.verify_extraction)
    print(f"v2_0_public_artifact: zip={zip_path}")
    print(f"v2_0_public_artifact: sha256={sha_path}")
    print(f"v2_0_public_artifact: files={file_count}")


if __name__ == "__main__":
    main()
