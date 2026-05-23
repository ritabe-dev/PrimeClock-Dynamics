"""Run lightweight PrimeClock Dynamics candidate workflows."""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any


def load_config(path: Path) -> dict[str, Any]:
    """Load a JSON workflow config."""
    try:
        config = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise SystemExit(f"invalid JSON workflow config: {path}: {exc}") from exc
    if not isinstance(config, dict):
        raise SystemExit("workflow config must be a JSON object")
    if "gates" not in config or not isinstance(config["gates"], dict):
        raise SystemExit("workflow config must contain a gates object")
    return config


def repo_root_from_config(config_path: Path) -> Path:
    """Return repository root inferred from a config under experiments/_workflow."""
    return config_path.resolve().parents[2]


def expand(value: str, *, python: str, tmp: Path) -> str:
    """Expand workflow placeholders."""
    return value.replace("{python}", python).replace("{tmp}", str(tmp))


def run_command(
    repo_root: Path,
    command_spec: dict[str, Any],
    *,
    python: str,
    tmp: Path,
) -> None:
    """Run one command specification."""
    command = command_spec.get("command")
    if not isinstance(command, list) or not all(isinstance(item, str) for item in command):
        raise SystemExit("workflow command must be a list of strings")

    cwd_value = command_spec.get("cwd", ".")
    if not isinstance(cwd_value, str):
        raise SystemExit("workflow cwd must be a string")
    cwd = (repo_root / expand(cwd_value, python=python, tmp=tmp)).resolve()
    if not cwd.is_dir():
        raise SystemExit(f"workflow cwd does not exist: {cwd}")

    expanded_command = [expand(item, python=python, tmp=tmp) for item in command]
    env = os.environ.copy()
    env_spec = command_spec.get("env", {})
    if not isinstance(env_spec, dict) or not all(
        isinstance(key, str) and isinstance(value, str) for key, value in env_spec.items()
    ):
        raise SystemExit("workflow env must be an object with string keys and values")
    for key, value in env_spec.items():
        env[key] = expand(value, python=python, tmp=tmp)
    completed = subprocess.run(
        expanded_command,
        cwd=cwd,
        env=env,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if completed.returncode != 0:
        raise SystemExit(
            "workflow command failed: "
            + " ".join(expanded_command)
            + f"\nstdout:\n{completed.stdout}\nstderr:\n{completed.stderr}"
        )

    expected_stdout = command_spec.get("expected_stdout")
    if expected_stdout is not None:
        if not isinstance(expected_stdout, str):
            raise SystemExit("expected_stdout must be a string")
        if expected_stdout not in completed.stdout:
            raise SystemExit(
                f"expected stdout fragment not found: {expected_stdout!r}\n"
                f"command: {' '.join(expanded_command)}\n"
                f"stdout:\n{completed.stdout}\nstderr:\n{completed.stderr}"
            )

    expected_file = command_spec.get("expected_file")
    if expected_file is not None:
        if not isinstance(expected_file, str):
            raise SystemExit("expected_file must be a string")
        expected_path = Path(expand(expected_file, python=python, tmp=tmp))
        if not expected_path.is_file():
            raise SystemExit(f"expected file was not created: {expected_path}")
        if expected_path.stat().st_size == 0:
            raise SystemExit(f"expected file is empty: {expected_path}")


def run_gate(config_path: Path, gate_name: str, *, python: str) -> None:
    """Run one named gate."""
    config = load_config(config_path)
    gates = config["gates"]
    if gate_name not in gates:
        available = ", ".join(sorted(gates))
        raise SystemExit(f"unknown gate {gate_name!r}; available gates: {available}")

    gate = gates[gate_name]
    if not isinstance(gate, dict):
        raise SystemExit(f"gate {gate_name!r} must be an object")
    commands = gate.get("commands")
    if not isinstance(commands, list):
        raise SystemExit(f"gate {gate_name!r} must contain a commands list")

    repo_root = repo_root_from_config(config_path)
    with tempfile.TemporaryDirectory(prefix="pcd-workflow-") as tmp_dir:
        tmp = Path(tmp_dir)
        for command_spec in commands:
            if not isinstance(command_spec, dict):
                raise SystemExit("each workflow command must be an object")
            run_command(repo_root, command_spec, python=python, tmp=tmp)

    candidate_id = config.get("candidate_id", config_path.stem)
    print(f"candidate gate: {gate_name}, candidate_id={candidate_id}, failed=0")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--python", default=sys.executable)
    parser.add_argument("gate")
    args = parser.parse_args()

    run_gate(args.config, args.gate, python=args.python)


if __name__ == "__main__":
    main()
