#!/usr/bin/env python3
"""Check PrimeClock Dynamics text hygiene and claim-boundary wording."""

from __future__ import annotations

import argparse
import re
from dataclasses import dataclass
from pathlib import Path


SCAN_ENTRIES = [
    "README.md",
    "docs",
    "experiments",
    "paper",
    "app/README.md",
    "app/src",
    "app/index.html",
]

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

SKIP_DIR_NAMES = {
    ".git",
    ".pytest_cache",
    ".ruff_cache",
    ".playwright-cli",
    "__pycache__",
    "dist",
    "node_modules",
}

SKIP_FILE_NAMES = {
    ".package-lock.json",
    "package-lock.json",
}

RULE_DOCUMENTATION_PATHS = {
    "docs/internal/TEXT_HYGIENE_POLICY.md",
}

CLAIM_BOUNDARY_PATHS = {
    "docs/CLAIM_BOUNDARY.md",
}

INTERNAL_POLICY_PREFIXES = (
    "docs/internal/",
)


@dataclass(frozen=True)
class TextRule:
    """One text hygiene rule."""

    name: str
    pattern: re.Pattern[str]
    category: str


@dataclass(frozen=True)
class Finding:
    """One text hygiene failure."""

    path: str
    line_number: int
    rule_name: str
    text: str

    def format(self) -> str:
        return f"{self.path}:{self.line_number}: {self.rule_name}: {self.text}"


CLAIM_RULES = [
    TextRule(
        "forbidden positive RH claim",
        re.compile(r"\bproves?\s+(?:the\s+)?Riemann hypothesis\b", re.IGNORECASE),
        "claim",
    ),
    TextRule(
        "forbidden prime-gap theorem claim",
        re.compile(r"\bprime[- ]gap theorem\b", re.IGNORECASE),
        "claim",
    ),
    TextRule(
        "forbidden prime-number-theorem proof claim",
        re.compile(r"\bproof\s+of\s+(?:the\s+)?prime number theorem\b", re.IGNORECASE),
        "claim",
    ),
    TextRule(
        "forbidden PRC theorem extension claim",
        re.compile(r"\bPRC theorem extensions?\b", re.IGNORECASE),
        "claim",
    ),
]

RELEASE_RULES = [
    TextRule(
        "forbidden official public release wording",
        re.compile(r"\bofficial public release\b", re.IGNORECASE),
        "release",
    ),
    TextRule(
        "forbidden Zenodo DOI wording",
        re.compile(r"\bZenodo DOI\b", re.IGNORECASE),
        "release",
    ),
    TextRule(
        "forbidden public-gate release wording",
        re.compile(r"\b" + "G" + r"ate\s+P\s+release\b", re.IGNORECASE),
        "release",
    ),
]

PROCESS_RULES = [
    TextRule("forbidden process wording", re.compile(r"\bChatGPT\b"), "process"),
    TextRule("forbidden process wording", re.compile(r"\bCodex\b"), "process"),
    TextRule("forbidden process wording", re.compile(r"\bLLM\b"), "process"),
    TextRule("forbidden process wording", re.compile(r"\bprompt\b", re.IGNORECASE), "process"),
    TextRule(
        "forbidden process wording",
        re.compile(r"\breview package\b", re.IGNORECASE),
        "process",
    ),
]

ALL_RULES = CLAIM_RULES + RELEASE_RULES + PROCESS_RULES


def repo_root_from_script() -> Path:
    """Return repository root inferred from this script."""
    return Path(__file__).resolve().parents[1]


def relative_text(path: Path, root: Path) -> str:
    """Return a POSIX relative path for display and rule matching."""
    return path.relative_to(root).as_posix()


def should_skip_path(path: Path, root: Path) -> bool:
    """Return true when a path is generated, dependency, cache, or unsupported text."""
    relative = path.relative_to(root)
    if any(part in SKIP_DIR_NAMES for part in relative.parts):
        return True
    if path.name in SKIP_FILE_NAMES:
        return True
    if path.is_file() and path.suffix not in TEXT_SUFFIXES:
        return True
    return False


def iter_text_paths(root: Path, entries: list[str] | None = None) -> list[Path]:
    """Return text files under the configured scan entries."""
    scan_entries = entries or SCAN_ENTRIES
    paths: list[Path] = []
    seen: set[Path] = set()
    for entry in scan_entries:
        source = root / entry
        if not source.exists():
            continue
        candidates = [source] if source.is_file() else sorted(source.rglob("*"))
        for path in candidates:
            if not path.is_file() or should_skip_path(path, root):
                continue
            resolved = path.resolve()
            if resolved in seen:
                continue
            seen.add(resolved)
            paths.append(path)
    return sorted(paths)


def is_internal_policy_path(relative_path: str) -> bool:
    """Return true for internal policy documents."""
    return any(relative_path.startswith(prefix) for prefix in INTERNAL_POLICY_PREFIXES)


def is_negated_line(line: str) -> bool:
    """Return true when a matching line is visibly boundary-setting."""
    lower = line.lower()
    return any(
        phrase in lower
        for phrase in [
            "does not claim",
            "do not claim",
            "does not make",
            "not a claim",
            "not a theorem",
            "not a public",
            "must not",
            "should not",
            "no ",
        ]
    )


def rule_is_allowed(relative_path: str, line_context: str, rule: TextRule) -> bool:
    """Return true when a rule match is allowed by boundary or internal context."""
    if relative_path in RULE_DOCUMENTATION_PATHS:
        return True
    if rule.category == "process" and is_internal_policy_path(relative_path):
        return True
    if rule.category in {"release", "process"} and is_negated_line(line_context):
        return True
    if rule.category == "claim" and relative_path in CLAIM_BOUNDARY_PATHS:
        return True
    if rule.category == "claim" and is_negated_line(line_context):
        return True
    return False


def scan_text(text: str, *, relative_path: str) -> list[Finding]:
    """Scan one text value and return findings."""
    findings: list[Finding] = []
    previous_line = ""
    for line_number, line in enumerate(text.splitlines(), start=1):
        line_context = f"{previous_line} {line}".strip()
        for rule in ALL_RULES:
            if not rule.pattern.search(line):
                continue
            if rule_is_allowed(relative_path, line_context, rule):
                continue
            findings.append(
                Finding(
                    path=relative_path,
                    line_number=line_number,
                    rule_name=rule.name,
                    text=line.strip(),
                )
            )
        previous_line = line
    return findings


def scan_root(root: Path, entries: list[str] | None = None) -> tuple[int, list[Finding]]:
    """Scan configured text files under ``root``."""
    files = iter_text_paths(root, entries=entries)
    findings: list[Finding] = []
    for path in files:
        relative_path = relative_text(path, root)
        text = path.read_text(encoding="utf-8")
        findings.extend(scan_text(text, relative_path=relative_path))
    return len(files), findings


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=repo_root_from_script())
    parser.add_argument(
        "--path",
        action="append",
        dest="paths",
        help="Optional scan entry relative to --root. May be passed more than once.",
    )
    args = parser.parse_args()

    root = args.root.resolve()
    checks, findings = scan_root(root, entries=args.paths)
    if findings:
        print("check_text_hygiene: failed")
        for finding in findings:
            print(f"FAIL: {finding.format()}")
        raise SystemExit(1)

    print(f"check_text_hygiene: checks={checks}, failed=0")


if __name__ == "__main__":
    main()
