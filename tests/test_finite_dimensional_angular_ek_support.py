from __future__ import annotations

from experiments._workflow.build_finite_dimensional_angular_ek_support import build_rows


def test_finite_dimensional_support_rows_are_pairwise() -> None:
    rows = build_rows()

    assert len(rows) == 3
    assert {row["angle_a"] for row in rows} | {row["angle_b"] for row in rows} == {
        "zero",
        "one_tenth",
        "sqrt2_mod1",
    }
    assert all(row["same_residue_primes_finite"] is True for row in rows)


def test_finite_dimensional_support_targets_are_stable() -> None:
    rows = build_rows()

    assert all(float(row["circular_distance"]) > 0 for row in rows)
    assert all(row["same_residue_prime_safe_bound"] >= 1 for row in rows)
    assert all(
        row["normalized_covariance_target"] == "off_diagonal_covariance/B_y^2 -> 0"
        for row in rows
    )
    assert all(row["cramer_wold_status"] == "gate_c_verified" for row in rows)
