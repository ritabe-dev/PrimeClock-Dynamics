from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def run_checker(env: dict[str, str] | None = None) -> subprocess.CompletedProcess[str]:
    merged_env = os.environ.copy()
    if env:
        merged_env.update(env)
    return subprocess.run(
        [sys.executable, "scripts/check_public_git_surface.py"],
        cwd=ROOT,
        env=merged_env,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )


def test_public_git_surface_checker_passes_current_checkout() -> None:
    completed = run_checker()
    assert completed.returncode == 0, completed.stdout + completed.stderr


def test_public_git_surface_allows_tool_named_head_ref() -> None:
    disclosed_ref = "feature/" + "co" + "dex" + "-disclosure"
    completed = run_checker({"GITHUB_HEAD_REF": disclosed_ref})
    assert completed.returncode == 0, completed.stdout + completed.stderr


def test_public_git_surface_allows_tool_named_pull_request_title(tmp_path: Path) -> None:
    event_path = tmp_path / "event.json"
    event_path.write_text(
        json.dumps(
            {
                "pull_request": {
                    "title": "Restore " + "Chat" + "GPT" + " note",
                    "head": {"ref": "release/public-artifact-protocol"},
                }
            }
        ),
        encoding="utf-8",
    )
    completed = run_checker({"GITHUB_EVENT_PATH": str(event_path)})
    assert completed.returncode == 0, completed.stdout + completed.stderr


def test_public_git_surface_blocks_local_path_head_ref() -> None:
    completed = run_checker({"GITHUB_HEAD_REF": "repair//Users/name/private"})
    assert completed.returncode != 0
    assert "forbidden local-path token" in completed.stdout
