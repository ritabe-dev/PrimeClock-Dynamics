#!/usr/bin/env python3
"""Check public Git metadata for process-tool wording."""

from __future__ import annotations

import json
import os
from pathlib import Path
import subprocess


ROOT = Path(__file__).resolve().parents[1]

FORBIDDEN_TERMS = (
    "co" + "dex",
    "chat" + "gpt",
    "open" + "ai",
    "ll" + "m",
)


def _run_git(args: list[str]) -> list[str]:
    completed = subprocess.run(
        ["git", *args],
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if completed.returncode != 0:
        raise SystemExit(completed.stderr.strip() or completed.stdout.strip())
    return [line.strip() for line in completed.stdout.splitlines() if line.strip()]


def _contains_forbidden(value: str) -> str | None:
    lower = value.lower()
    for term in FORBIDDEN_TERMS:
        if term in lower:
            return term
    return None


def _check_value(label: str, value: str, failures: list[str]) -> None:
    term = _contains_forbidden(value)
    if term is not None:
        failures.append(f"{label} contains forbidden public-process token: {term}")


def _event_values() -> list[tuple[str, str]]:
    values: list[tuple[str, str]] = []
    event_path = os.environ.get("GITHUB_EVENT_PATH")
    if not event_path:
        return values
    path = Path(event_path)
    if not path.is_file():
        return values
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise SystemExit(f"invalid GitHub event JSON: {exc}") from exc

    pull_request = data.get("pull_request")
    if isinstance(pull_request, dict):
        title = pull_request.get("title")
        if isinstance(title, str):
            values.append(("pull request title", title))
        head = pull_request.get("head")
        if isinstance(head, dict):
            ref = head.get("ref")
            if isinstance(ref, str):
                values.append(("pull request head ref", ref))
    return values


def collect_values() -> list[tuple[str, str]]:
    values: list[tuple[str, str]] = []
    for name in ["GITHUB_HEAD_REF", "GITHUB_REF_NAME", "GITHUB_BASE_REF"]:
        value = os.environ.get(name)
        if value:
            values.append((name, value))

    try:
        current_branch = _run_git(["branch", "--show-current"])
    except SystemExit:
        current_branch = []
    if current_branch:
        values.append(("current branch", current_branch[0]))

    for ref in _run_git(["for-each-ref", "--format=%(refname:short)", "refs/heads", "refs/remotes"]):
        values.append(("git ref", ref))

    for subject in _run_git(["log", "--format=%s", "-20"]):
        values.append(("recent commit subject", subject))

    values.extend(_event_values())
    return values


def main() -> None:
    failures: list[str] = []
    for label, value in collect_values():
        _check_value(label, value, failures)
    if failures:
        print("check_public_git_surface: failed")
        for failure in failures:
            print(f"FAIL: {failure}")
        raise SystemExit(1)
    print("check_public_git_surface: checks=public-git-metadata, failed=0")


if __name__ == "__main__":
    main()
