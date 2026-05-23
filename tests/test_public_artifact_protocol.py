from __future__ import annotations

import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_public_artifact_protocol_checker_passes() -> None:
    completed = subprocess.run(
        [sys.executable, "scripts/check_public_artifact_protocol.py"],
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    assert completed.returncode == 0, completed.stdout + completed.stderr


def test_known_public_versions_have_frozen_source_surfaces() -> None:
    for version in ["v0.2.0", "v1.0.0", "v1.1.0", "v2.0.0"]:
        version_dir = ROOT / "artifacts" / version
        assert (version_dir / "ARTIFACT_MANIFEST.json").is_file()
        assert (version_dir / "RELEASE_NOTES.md").is_file()
        assert (version_dir / "CITATION.cff").is_file()
        assert (version_dir / "source" / "README.md").is_file()
