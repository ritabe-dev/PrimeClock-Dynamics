from __future__ import annotations

import math
from fractions import Fraction

from experiments.akc.run_collision_kernel_by_scale import build_rows
from prime_clock_dynamics.collision_kernel import (
    collision_kernel,
    collision_kernel_term,
    kernel_matrix,
    selected_residue_exact,
)
from prime_clock_dynamics.multiplicity import multiplicity_covariance_baseline
from prime_clock_dynamics.primes import primes_up_to


def test_collision_kernel_matches_existing_covariance_baseline() -> None:
    primes = primes_up_to(50)
    alpha = Fraction(1, 10)
    beta = Fraction(3, 10)
    assert collision_kernel(primes, alpha, beta) == multiplicity_covariance_baseline(
        alpha,
        beta,
        primes,
    )


def test_kernel_matrix_diagonal_is_variance() -> None:
    primes = primes_up_to(30)
    angles = [Fraction(0), Fraction(1, 10), Fraction(2, 5)]
    matrix = kernel_matrix(primes, angles)
    for index, angle in enumerate(angles):
        assert matrix[index][index] == multiplicity_covariance_baseline(angle, angle, primes)


def test_kernel_matrix_is_symmetric() -> None:
    primes = primes_up_to(50)
    angles = [Fraction(0), Fraction(1, 12), Fraction(7, 24), Fraction(5, 6)]
    matrix = kernel_matrix(primes, angles)
    for row_index, row in enumerate(matrix):
        for column_index, value in enumerate(row):
            assert value == matrix[column_index][row_index]


def test_selected_residue_exact_uses_half_open_boundary_convention() -> None:
    assert selected_residue_exact(Fraction(1, 10), 5) == 1
    assert selected_residue_exact(Fraction(9, 10), 5) == 0
    assert selected_residue_exact(Fraction(-1, 10), 5) == 0
    assert selected_residue_exact(Fraction(11, 10), 5) == 1


def test_normalized_kernel_matrix_is_psd_for_small_angle_lists() -> None:
    cases = [
        (primes_up_to(30), [Fraction(0), Fraction(1, 9), Fraction(2, 9)]),
        (primes_up_to(50), [Fraction(1, 20), Fraction(3, 20), Fraction(7, 20)]),
    ]
    for primes, angles in cases:
        matrix = kernel_matrix(primes, angles)
        variances = [matrix[index][index] for index in range(len(angles))]
        normalized = [
            [
                matrix[row][column] / _shared_variance(variances[row], variances[column])
                for column in range(len(angles))
            ]
            for row in range(len(angles))
        ]
        for index in range(len(angles)):
            assert normalized[index][index] == Fraction(1)
        for row in range(len(angles)):
            for column in range(row + 1, len(angles)):
                assert normalized[row][column] == normalized[column][row]
                assert Fraction(1) - normalized[row][column] ** 2 >= 0
        assert _determinant_3x3(normalized) >= 0


def test_collision_kernel_by_scale_rows_have_expected_schema_and_values() -> None:
    rows = build_rows()
    expected_keys = {
        "cutoff",
        "theta",
        "prime_count",
        "same_residue_prime_count",
        "variance_B2",
        "collision_kernel",
        "correlation_ratio",
        "distance_heuristic_ratio",
        "status",
    }
    assert len(rows) == 9
    assert rows == build_rows()
    for row in rows:
        assert set(row) == expected_keys
        assert row["cutoff"] in {100, 1000, 5000}
        assert row["theta"] in {0.25, 0.5, 0.75}
        assert isinstance(row["prime_count"], int)
        assert isinstance(row["same_residue_prime_count"], int)
        assert 0 <= row["same_residue_prime_count"] <= row["prime_count"]
        assert row["variance_B2"] > 0.0
        assert math.isfinite(row["collision_kernel"])
        assert math.isfinite(row["correlation_ratio"])
        assert -1.0 <= row["correlation_ratio"] <= 1.0
        assert 0.0 <= row["distance_heuristic_ratio"] <= 1.0
        assert row["status"] == "kernel_diagnostic"


def test_zero_ray_equal_residue_threshold_is_exact() -> None:
    delta = Fraction(1, 20)
    for p in primes_up_to(100):
        same_residue = selected_residue_exact(Fraction(0), p) == selected_residue_exact(delta, p)
        assert same_residue == (p * delta < Fraction(1, 2))


def test_zero_ray_kernel_matches_threshold_formula() -> None:
    primes = primes_up_to(100)
    delta = Fraction(1, 20)
    direct_kernel = collision_kernel(primes, Fraction(0), delta)
    threshold_kernel = sum(
        (
            Fraction(1, p) - Fraction(1, p * p)
            if p * delta < Fraction(1, 2)
            else -Fraction(1, p * p)
        )
        for p in primes
    )
    term_kernel = sum((collision_kernel_term(Fraction(0), delta, p) for p in primes), Fraction(0))
    assert direct_kernel == threshold_kernel
    assert direct_kernel == term_kernel


def _shared_variance(left: Fraction, right: Fraction) -> Fraction:
    assert left == right
    assert left > 0
    return left


def _determinant_3x3(matrix: list[list[Fraction]]) -> Fraction:
    return (
        matrix[0][0] * matrix[1][1] * matrix[2][2]
        + matrix[0][1] * matrix[1][2] * matrix[2][0]
        + matrix[0][2] * matrix[1][0] * matrix[2][1]
        - matrix[0][2] * matrix[1][1] * matrix[2][0]
        - matrix[0][1] * matrix[1][0] * matrix[2][2]
        - matrix[0][0] * matrix[1][2] * matrix[2][1]
    )
