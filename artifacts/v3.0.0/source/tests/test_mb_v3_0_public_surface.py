from __future__ import annotations

from pathlib import Path

from experiments.mb.run_mb_v3_0_public_support import build_support
from scripts import build_v3_0_public_artifact as public_builder


ROOT = Path(__file__).resolve().parents[1]


def test_v3_0_public_support_is_focused(tmp_path) -> None:
    summary = build_support(tmp_path)
    assert summary["profile"] == "v3_0_mertens_boundary_public_support"
    assert summary["experiment_count"] == 6
    assert summary["public_artifact_support"] is True
    assert summary["public_release_claimed"] is True
    assert summary["doi_claimed"] is False
    assert summary["zenodo_claimed"] is False
    assert summary["integer_time_transfer_claimed"] is False
    assert summary["diagonal_mertens_claimed"] is False
    assert summary["high_point_theorem_claimed"] is False
    for item in summary["experiments"]:
        text = (tmp_path / item["file"]).read_text(encoding="utf-8")
        assert "public_" in text
        assert "gate_c_" not in text
        assert "gate_r_" not in text


def test_v3_0_public_builder_excludes_internal_surfaces() -> None:
    builder_text = (ROOT / "scripts/build_v3_0_public_artifact.py").read_text(encoding="utf-8")
    assert "paper/primeclock_dynamics_v3_0_release_manuscript.md" in public_builder.INCLUDE_EXACT
    assert "docs/MB_V3_0_RELEASE_CLAIM_BOUNDARY.md" in public_builder.INCLUDE_EXACT
    assert "experiments/mb/run_mb_v3_0_support.py" in public_builder.INCLUDE_EXACT
    assert "experiments/mb/run_mb_v3_0_public_support.py" in public_builder.INCLUDE_EXACT
    assert "experiments/_workflow/pcd_v3_0_public_artifact.json" in public_builder.INCLUDE_EXACT
    assert "paper/mertens_boundary_v3_0_gate_c.md" in public_builder.FORBIDDEN_MEMBERS
    assert "paper/mertens_boundary_v3_0_gate_r.md" in public_builder.FORBIDDEN_MEMBERS
    assert "experiments/mb/run_mb_v3_0_gate_c_support.py" in public_builder.FORBIDDEN_MEMBERS
    assert "experiments/mb/run_mb_v3_0_gate_r_support.py" in public_builder.FORBIDDEN_MEMBERS
    assert "support_base" not in builder_text
