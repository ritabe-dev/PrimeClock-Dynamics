from __future__ import annotations

import json
from pathlib import Path

from experiments.it.run_v3_5_public_support import write_outputs


ROOT = Path(__file__).resolve().parents[1]


def first_existing(*paths: Path) -> Path:
    for path in paths:
        if path.is_file():
            return path
    return paths[0]


def test_v3_5_public_surface_files() -> None:
    required = [
        "RELEASE_NOTES_v3_5_0.md",
        "ARTIFACT_MANIFEST_v3_5_0.json",
        "docs/IT_V3_5_PUBLIC_CLAIM_BOUNDARY.md",
        "paper/primeclock_dynamics_v3_5_public_manuscript.md",
        "experiments/_workflow/pcd_v3_5_public_artifact.json",
        "experiments/it/_workflow/check_v3_5_public_artifact.py",
        "scripts/build_v3_5_public_artifact.py",
    ]
    assert first_existing(ROOT / "README_V3_5_0_PUBLIC.md", ROOT / "README.md").is_file()
    assert first_existing(ROOT / "CITATION_v3_5_0_PUBLIC.cff", ROOT / "CITATION.cff").is_file()
    for relative in required:
        assert (ROOT / relative).is_file()


def test_v3_5_public_workflow_boundary() -> None:
    workflow = json.loads(
        (ROOT / "experiments/_workflow/pcd_v3_5_public_artifact.json").read_text(
            encoding="utf-8"
        )
    )
    assert workflow["candidate_id"] == "pcd_v3_5_public_artifact"
    assert workflow["status"] == "public_artifact"
    assert workflow["public_release"] is True
    assert {"quick", "support", "bundle"}.issubset(workflow["gates"])


def test_v3_5_public_support_summary_nonclaims(tmp_path: Path) -> None:
    summary = write_outputs(tmp_path / "support")
    assert summary["experiment_count"] == 5
    assert summary["row_count"] == 31
    assert summary["public_artifact_support"] is True
    assert summary["public_release_claimed"] is True
    assert summary["doi_claimed"] is False
    assert summary["zenodo_claimed"] is False
    assert summary["full_diagonal_claimed"] is False
    assert summary["distributional_diagonal_claimed"] is False
    assert summary["conductor_tail_theorem_claimed"] is False
    assert summary["all_tv_bounds_passed"] is True
    assert summary["all_bounded_test_bounds_passed"] is True
    assert summary["all_moment_bounds_passed"] is True


def test_v3_5_public_support_statuses_are_focused(tmp_path: Path) -> None:
    write_outputs(tmp_path / "support")
    for path in (tmp_path / "support").glob("*.csv"):
        text = path.read_text(encoding="utf-8")
        assert "public_" in text
        assert "gate_" + "p_" not in text
        assert "gate_" + "c_" not in text
        assert "gate_" + "r_" not in text
