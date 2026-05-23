from __future__ import annotations

from pathlib import Path

from experiments.akc.run_akc_v2_0_public_support import build_support
from scripts import build_v2_0_public_artifact as public_builder


ROOT = Path(__file__).resolve().parents[1]


def test_v2_0_public_support_is_focused(tmp_path) -> None:
    summary = build_support(tmp_path)
    assert summary["profile"] == "v2_0_akc_public_support"
    assert summary["experiment_count"] == 6
    assert summary["public_artifact_support"] is True
    assert summary["public_release_claimed"] is True
    assert summary["doi_claimed"] is False
    assert summary["zenodo_claimed"] is False
    assert summary["negative_beta_boundary_claimed"] is False
    assert summary["high_point_theorem_claimed"] is False
    names = [item["name"] for item in summary["experiments"]]
    assert "07_negative_beta_boundary_diagnostic" not in names
    assert "08_positive_beta_high_point_diagnostic" not in names
    for item in summary["experiments"]:
        text = (tmp_path / item["file"]).read_text(encoding="utf-8")
        assert "public_" in text
        assert "gate_" + "p_" not in text
        assert "gate_" + "c_" not in text
        assert "gate_" + "r_" not in text


def test_v2_0_public_builder_excludes_internal_surfaces() -> None:
    builder_text = (ROOT / "scripts/build_v2_0_public_artifact.py").read_text(encoding="utf-8")
    assert "paper/primeclock_dynamics_v2_0_public_manuscript.md" in public_builder.INCLUDE_EXACT
    assert "experiments/akc/run_akc_v2_0_public_support.py" in public_builder.INCLUDE_EXACT
    assert "experiments/_workflow/pcd_v2_0_public_artifact.json" in public_builder.INCLUDE_EXACT
    assert "experiments/_workflow/pcd_v2_0_akc_gate_" + "c.json" not in public_builder.INCLUDE_EXACT
    assert "experiments/_workflow/pcd_v2_0_akc_gate_" + "r.json" not in public_builder.INCLUDE_EXACT
    assert "experiments/akc/run_akc_v2_0_gate_" + "r_experiments.py" in public_builder.FORBIDDEN_MEMBERS
    assert "support_base" not in builder_text
