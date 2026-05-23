from __future__ import annotations

from fractions import Fraction

from prime_clock_dynamics.mertens_boundary import (
    cell_polynomial_coefficients,
    hard_q_point_factor,
    hard_q_point_local_factor,
    hard_two_point_local_factor,
    hard_weight,
    mertens_product,
)
from prime_clock_dynamics.multiplicity import selected_residue
from prime_clock_dynamics.primes import primes_up_to


def test_hard_one_prime_weight_normalizes() -> None:
    p = 7
    alpha = Fraction(1, 10)
    selected = selected_residue(alpha, p)
    expectation = sum(hard_weight(residue == selected, p) for residue in range(p)) / p
    assert expectation == 1


def test_hard_q_point_local_factor_matches_formula_cases() -> None:
    assert hard_q_point_local_factor(5, [Fraction(0)]) == 1
    assert hard_two_point_local_factor(5, Fraction(0), Fraction(1, 2)) == Fraction(15, 16)
    assert hard_two_point_local_factor(5, Fraction(0), Fraction(1, 100)) == Fraction(5, 4)


def test_hard_q_point_product_exact_type() -> None:
    primes = primes_up_to(7)
    value = hard_q_point_factor(primes, [Fraction(0), Fraction(1, 9)])
    assert isinstance(value, Fraction)
    assert value >= 0


def test_cell_polynomial_coefficients_sum_to_one() -> None:
    primes = primes_up_to(7)
    residues = {p: 0 for p in primes}
    coefficients = cell_polynomial_coefficients(residues, primes)
    assert sum(coefficients.values()) == 1
    assert coefficients.get(0, Fraction(0)) >= 0
    assert mertens_product(primes) > 0
