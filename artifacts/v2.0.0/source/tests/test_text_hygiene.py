from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import check_text_hygiene


def write_file(root: Path, relative_path: str, text: str) -> Path:
    path = root / relative_path
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return path


def test_claim_boundary_non_claims_are_allowed(tmp_path: Path) -> None:
    write_file(
        tmp_path,
        "docs/CLAIM_BOUNDARY.md",
        "\n".join(
            [
                "# Claim Boundary",
                "It does not claim:",
                "- a result about the Riemann hypothesis;",
                "- a proof of the prime number theorem;",
                "- a PRC theorem extension;",
            ]
        ),
    )

    checks, findings = check_text_hygiene.scan_root(tmp_path, entries=["docs"])

    assert checks == 1
    assert findings == []


def test_positive_major_theorem_claim_is_blocked(tmp_path: Path) -> None:
    write_file(tmp_path, "README.md", "This proves the Riemann hypothesis.\n")

    checks, findings = check_text_hygiene.scan_root(tmp_path, entries=["README.md"])

    assert checks == 1
    assert len(findings) == 1
    assert findings[0].rule_name == "forbidden positive RH claim"


def test_generated_app_outputs_and_lockfiles_are_ignored(tmp_path: Path) -> None:
    write_file(tmp_path, "README.md", "# Safe\n")
    write_file(tmp_path, "app/dist/index.html", "This proves the Riemann hypothesis.\n")
    write_file(tmp_path, "app/package-lock.json", '{"note": "ChatGPT prompt"}\n')

    checks, findings = check_text_hygiene.scan_root(
        tmp_path,
        entries=["README.md", "app"],
    )

    assert checks == 1
    assert findings == []


def test_cli_reports_failures(tmp_path: Path) -> None:
    write_file(tmp_path, "README.md", "This is a prime gap theorem.\n")

    completed = subprocess.run(
        [
            sys.executable,
            "scripts/check_text_hygiene.py",
            "--root",
            str(tmp_path),
            "--path",
            "README.md",
        ],
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )

    assert completed.returncode != 0
    assert "check_text_hygiene: failed" in completed.stdout
    assert "forbidden prime-gap theorem claim" in completed.stdout


def test_real_workflow_config_runs_text_hygiene() -> None:
    workflows = sorted((ROOT / "experiments/_workflow").glob("*.json"))
    assert workflows
    assert any(
        "scripts/check_text_hygiene.py" in workflow.read_text(encoding="utf-8")
        for workflow in workflows
    )
