#!/usr/bin/env python3
"""Check the version-generic public artifact preservation protocol."""

from __future__ import annotations

import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ARTIFACTS = ROOT / "artifacts"
sys.path.insert(0, str(ROOT / "scripts"))
from build_artifact import SUPPORTED_VERSIONS  # noqa: E402
VERSION_RE = re.compile(r"^v\d+\.\d+\.\d+$")

REQUIRED_ROOT_FILES = {
    "ARTIFACT_MANIFEST.json",
    "RELEASE_NOTES.md",
    "CITATION.cff",
}
REQUIRED_SOURCE_FILES = {
    "README.md",
    "LICENSE",
    "pyproject.toml",
    "setup.py",
}
FORBIDDEN_NAMES = {
    ".DS_Store",
    ".pytest_cache",
    "__pycache__",
}


def fail(message: str) -> None:
    raise SystemExit(f"check_public_artifact_protocol: FAIL: {message}")


def version_key(path: Path) -> tuple[int, int, int]:
    major, minor, patch = path.name.removeprefix("v").split(".")
    return int(major), int(minor), int(patch)


def check_no_forbidden_generated_files(version_dir: Path) -> None:
    for path in version_dir.rglob("*"):
        if path.name in FORBIDDEN_NAMES:
            fail(f"{version_dir.name} contains generated/cache path: {path.relative_to(ROOT)}")


def check_public_version(version_dir: Path) -> None:
    version_no_v = version_dir.name.removeprefix("v")
    if version_no_v not in SUPPORTED_VERSIONS:
        fail(f"{version_dir.name} is not supported by scripts/build_artifact.py")

    missing = sorted(name for name in REQUIRED_ROOT_FILES if not (version_dir / name).is_file())
    if missing:
        fail(f"{version_dir.name} missing root metadata files: {missing}")

    source = version_dir / "source"
    if not source.is_dir():
        fail(f"{version_dir.name} missing frozen source directory: {source.relative_to(ROOT)}")

    missing_source = sorted(name for name in REQUIRED_SOURCE_FILES if not (source / name).is_file())
    if missing_source:
        fail(f"{version_dir.name} frozen source missing files: {missing_source}")

    parts = version_no_v.split(".")
    builder_names = {
        f"build_v{version_no_v.replace('.', '_')}_public_artifact.py",
        f"build_v{parts[0]}_{parts[1]}_public_artifact.py",
    }
    if not any((source / "scripts" / name).is_file() for name in builder_names):
        fail(
            f"{version_dir.name} frozen source missing version builder; "
            f"expected one of {sorted(builder_names)}"
        )

    if (version_dir / "DOI_RECORD.md").is_file() and not (version_dir / "SHA256SUMS.txt").is_file():
        fail(f"{version_dir.name} has DOI_RECORD.md but no SHA256SUMS.txt")

    check_no_forbidden_generated_files(version_dir)


def main() -> None:
    if not ARTIFACTS.is_dir():
        fail("artifacts directory missing")

    version_dirs = sorted(
        (path for path in ARTIFACTS.iterdir() if path.is_dir() and VERSION_RE.match(path.name)),
        key=version_key,
    )
    if not version_dirs:
        fail("no versioned artifact directories found")

    for version_dir in version_dirs:
        check_public_version(version_dir)

    print(f"check_public_artifact_protocol: versions={len(version_dirs)}, failed=0")


if __name__ == "__main__":
    main()
