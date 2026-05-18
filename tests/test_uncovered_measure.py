from fractions import Fraction
from math import isclose

import pytest

from prime_clock_dynamics.uncovered import (
    cutoff_mertens_product_baseline,
    cutoff_uncovered_measure,
    diagonal_uncovered_measure_for_primes,
    mertens_product_baseline,
    poisson_baseline,
    residue_uncovered_measure_for_primes,
    uncovered_measure,
    uncovered_measure_for_primes,
)


def test_uncovered_measure_small_values() -> None:
    assert uncovered_measure(2) == Fraction(1, 2)
    assert uncovered_measure(3) == Fraction(1, 6)


def test_uncovered_measure_is_normalized() -> None:
    for n in range(2, 200):
        measure = uncovered_measure(n)
        assert Fraction(0) <= measure <= Fraction(1)


def test_baselines_are_normalized() -> None:
    for n in [2, 3, 10, 100]:
        assert 0 < mertens_product_baseline(n) <= 1
        assert 0 < poisson_baseline(n) <= 1


def test_cutoff_uncovered_measure_uses_fixed_prime_set() -> None:
    assert cutoff_uncovered_measure(2, 3) == residue_uncovered_measure_for_primes(2, [2, 3])
    assert cutoff_uncovered_measure(2, 3) != uncovered_measure(2)
    assert isclose(cutoff_mertens_product_baseline(3), (1.0 / 2.0) * (2.0 / 3.0))


def test_cutoff_uncovered_measure_allows_crt_residue_times() -> None:
    assert isinstance(cutoff_uncovered_measure(0, 3), Fraction)
    assert isinstance(cutoff_uncovered_measure(1, 3), Fraction)
    assert isinstance(residue_uncovered_measure_for_primes(0, [2, 3]), Fraction)
    assert isinstance(residue_uncovered_measure_for_primes(1, [2, 3]), Fraction)


def test_cutoff_uncovered_measure_complete_crt_period_includes_zero() -> None:
    rows = [cutoff_uncovered_measure(n, 3) for n in range(6)]
    assert len(rows) == 6
    assert all(Fraction(0) <= value <= Fraction(1) for value in rows)


def test_diagonal_uncovered_measure_rejects_non_app_times() -> None:
    with pytest.raises(ValueError, match="n must be >= 2"):
        uncovered_measure(0)
    with pytest.raises(ValueError, match="n must be >= 2"):
        diagonal_uncovered_measure_for_primes(0, [2, 3])
    with pytest.raises(ValueError, match="n must be >= 2"):
        uncovered_measure_for_primes(0, [2, 3])


def test_uncovered_measure_for_primes_remains_diagonal_alias() -> None:
    assert uncovered_measure_for_primes(2, [2, 3]) == diagonal_uncovered_measure_for_primes(
        2, [2, 3]
    )
