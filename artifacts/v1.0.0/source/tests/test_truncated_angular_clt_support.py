from experiments._workflow.build_truncated_angular_clt_support import build_rows


def test_truncated_angular_clt_support_rows_smoke() -> None:
    rows = build_rows()
    assert len(rows) == 3
    assert rows == build_rows()
    assert [row["moment_order"] for row in rows] == [2, 3, 4]
    assert {
        "window_size",
        "cutoff",
        "moment_order",
        "prime_count",
        "variance",
        "cutoff_power_over_window",
        "prime_count_power_over_window",
        "prime_count_power_over_window_variance_scale",
        "satisfies_y_power_budget",
        "satisfies_prime_count_budget",
        "satisfies_normalized_prime_count_budget",
    } <= set(rows[0])
    assert all(float(row["variance"]) > 0.0 for row in rows)
    assert all(float(row["prime_count_power_over_window_variance_scale"]) >= 0.0 for row in rows)
    assert all(row["satisfies_y_power_budget"] for row in rows)
    assert all(row["satisfies_prime_count_budget"] for row in rows)
    assert all(row["satisfies_normalized_prime_count_budget"] for row in rows)
    assert (
        rows[0]["cutoff_power_over_window"]
        > rows[1]["cutoff_power_over_window"]
        > rows[2]["cutoff_power_over_window"]
    )
