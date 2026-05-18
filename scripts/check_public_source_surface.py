#!/usr/bin/env python3
"""Check that public source and release ZIP surfaces stay minimal."""

from __future__ import annotations

import argparse
import re
import subprocess
from pathlib import Path
import zipfile


ROOT = Path(__file__).resolve().parents[1]

TEXT_SUFFIXES = {
    ".cff",
    ".css",
    ".html",
    ".js",
    ".json",
    ".jsx",
    ".md",
    ".py",
    ".toml",
    ".txt",
    ".yml",
    ".yaml",
}


def word(*parts: str) -> str:
    """Join string pieces while keeping sensitive terms out of this source."""
    return "".join(parts)


FORBIDDEN_PATH_PARTS = [
    "docs/internal/",
    "docs/ROADMAP.md",
    "app/",
    "data/",
    "notebooks/",
    "experiments/angular_erdos_kac/",
    "experiments/mertens_uncovered_measure/",
    "experiments/random_model_controls/",
    "paper/diagonal_bridge_packet_v0_3.md",
    "paper/random_nonrandom_packet_v0_4.md",
    "paper/prime_clock_angular_sieve_note_v0_1.md",
    "scripts/build_" + word("ga", "te") + "_",
    word("GA", "TE_"),
    word("ga", "te_c"),
    word("PROPOSITION", "_STATUS"),
    word("REVIEW", "ER"),
    word("REVIEW", "_REQUEST"),
    word("PUBLIC", "_WORDING"),
    word("V0_2_", "VERIFICATION"),
    "V0_" + "3_",
    "V0_" + "4_",
]

FORBIDDEN_TEXT_PATTERNS = [
    word("Ga", "te") + r"\s+[RCP]\b",
    word("GA", "TE_"),
    word("ga", "te_c"),
    word("PROPOSITION", "_STATUS"),
    word("REVIEW", "ER"),
    word("REVIEW", "_REQUEST"),
    word("PUBLIC", "_WORDING"),
    word("V0_2_", "VERIFICATION"),
    "V0_" + "3_",
    "V0_" + "4_",
    r"\u30b9\u30e9\u30a4\u30b9",
    "Current " + "completion",
    "mathematical " + "impact",
    r"\u4f5c\u696d\u30ec\u30dd\u30fc\u30c8",
]

TEXT_PATTERN = re.compile("|".join(f"(?:{pattern})" for pattern in FORBIDDEN_TEXT_PATTERNS))


def tracked_files(root: Path) -> list[str]:
    """Return tracked files in stable order."""
    completed = subprocess.run(
        ["git", "ls-files"],
        cwd=root,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if completed.returncode != 0:
        raise SystemExit(completed.stderr)
    return [line for line in completed.stdout.splitlines() if line]


def check_path(name: str, failures: list[str]) -> None:
    """Check one relative path."""
    for marker in FORBIDDEN_PATH_PARTS:
        if name == marker.rstrip("/") or name.startswith(marker):
            failures.append(f"{name}: forbidden public source path")
            return


def check_text(name: str, text: str, failures: list[str]) -> None:
    """Check one text value."""
    for line_number, line in enumerate(text.splitlines(), start=1):
        if TEXT_PATTERN.search(line):
            failures.append(f"{name}:{line_number}: forbidden public source wording: {line.strip()}")
            return


def check_source(root: Path) -> list[str]:
    """Check the tracked public source tree."""
    failures: list[str] = []
    for name in tracked_files(root):
        check_path(name, failures)
        path = root / name
        if path.suffix in TEXT_SUFFIXES:
            check_text(name, path.read_text(encoding="utf-8"), failures)
    return failures


def check_zip(zip_path: Path) -> list[str]:
    """Check public release ZIP members."""
    failures: list[str] = []
    with zipfile.ZipFile(zip_path) as archive:
        for name in archive.namelist():
            relative = name.split("/", 1)[1] if "/" in name else name
            check_path(relative, failures)
            if Path(relative).suffix in TEXT_SUFFIXES:
                check_text(relative, archive.read(name).decode("utf-8", "ignore"), failures)
    return failures


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--zip", type=Path)
    args = parser.parse_args()

    failures = check_zip(args.zip) if args.zip else check_source(ROOT)
    if failures:
        print("check_public_source_surface: failed")
        for failure in failures:
            print(f"FAIL: {failure}")
        raise SystemExit(1)
    print("check_public_source_surface: checks=1, failed=0")


if __name__ == "__main__":
    main()
