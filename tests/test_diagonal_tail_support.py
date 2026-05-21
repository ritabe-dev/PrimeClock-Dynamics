from experiments._workflow.build_diagonal_tail_support import build_rows


def test_diagonal_tail_support_rows_smoke() -> None:
    rows = build_rows()
    assert len(rows) == 3
    assert rows == build_rows()
    assert [row["moment_order"] for row in rows] == [2, 3, 4]
    assert all(row["truncation"] == "floor(N^(1/loglogN))" for row in rows)
    assert all(row["theta_fraction"] == "1/loglogN" for row in rows)
    assert {
        "window_size",
        "dyadic_start",
        "dyadic_end",
        "moment_order",
        "truncation",
        "theta_fraction",
        "theta",
        "cutoff",
        "cutoff_prime_count",
        "dyadic_prime_count",
        "cutoff_variance",
        "dyadic_variance",
        "dyadic_scale",
        "loglog_window",
        "cutoff_power_over_window",
        "cutoff_power_budget_exponent",
        "prime_count_power_over_window_variance_scale",
        "tail_prime_harmonic",
        "tail_mean_over_dyadic_scale",
        "centering_gap_A_2N_minus_A_y",
        "centering_gap_over_dyadic_scale",
        "scale_ratio_B_y_over_B_2N",
        "v0_6_y_power_budget_asymptotic",
        "tail_l1_markov_target",
        "uses_tail_moment_bound",
    } <= set(rows[0])
    assert all(int(row["cutoff"]) >= 2 for row in rows)
    assert all(float(row["cutoff_variance"]) > 0.0 for row in rows)
    assert all(float(row["dyadic_variance"]) > 0.0 for row in rows)
    assert all(float(row["tail_prime_harmonic"]) >= 0.0 for row in rows)
    assert all(float(row["tail_mean_over_dyadic_scale"]) >= 0.0 for row in rows)
    assert all(float(row["centering_gap_over_dyadic_scale"]) >= 0.0 for row in rows)
    assert all(0 < float(row["scale_ratio_B_y_over_B_2N"]) <= 1.0 for row in rows)
    assert all(row["v0_6_y_power_budget_asymptotic"] for row in rows)
    assert all(row["tail_l1_markov_target"] == "E[T_y]/B_2N -> 0" for row in rows)
    assert all(row["uses_tail_moment_bound"] is False for row in rows)
    assert all(isinstance(row["tail_prime_harmonic"], str) for row in rows)
