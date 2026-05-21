from experiments._workflow.build_diagonal_angular_ek_support import build_rows


def test_diagonal_angular_ek_support_rows_smoke() -> None:
    rows = build_rows()
    assert len(rows) == 3
    assert rows == build_rows()
    assert [row["moment_order"] for row in rows] == [2, 3, 4]
    assert {
        "window_start_N",
        "window_end_2N",
        "moment_order",
        "slow_cutoff_y",
        "prime_count_pi_y",
        "truncation",
        "y_power_over_N",
        "v0_6_fixed_order_budget_asymptotic",
        "finite_row_y_power_budget_below_one",
        "cutoff_variance_B_y_squared",
        "dyadic_variance_asymptotic",
        "scale_ratio_B_y_over_B_2N",
        "tail_prime_harmonic_asymptotic",
        "tail_mean_over_dyadic_scale",
        "centering_gap_over_dyadic_scale",
        "slutsky_tail_target",
        "assembly_status",
    } <= set(rows[0])
    assert all(row["truncation"] == "floor(N^(1/loglogN))" for row in rows)
    assert all(row["v0_6_fixed_order_budget_asymptotic"] for row in rows)
    assert any(row["finite_row_y_power_budget_below_one"] for row in rows)
    assert all(float(row["y_power_over_N"]) >= 0.0 for row in rows)
    assert all(float(row["cutoff_variance_B_y_squared"]) > 0.0 for row in rows)
    assert all(float(row["dyadic_variance_asymptotic"]) > 0.0 for row in rows)
    assert all(0.0 < float(row["scale_ratio_B_y_over_B_2N"]) <= 1.0 for row in rows)
    assert all(float(row["tail_mean_over_dyadic_scale"]) >= 0.0 for row in rows)
    assert all(row["slutsky_tail_target"] == "T_y/B_2N -> 0 in probability" for row in rows)
    assert all(row["assembly_status"] == "gate_c_verified_support" for row in rows)
