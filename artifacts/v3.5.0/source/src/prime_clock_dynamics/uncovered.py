"""Uncovered-measure helpers for PrimeClock Dynamics."""

from __future__ import annotations

import math
from fractions import Fraction
from typing import Iterable

from .intervals import complement_intervals, split_circular_interval, total_measure
from .multiplicity import diagonal_center, residue_center
from .primes import primes_up_to


def _prime_values_for_cutoff(cutoff: int) -> list[int]:
    if isinstance(cutoff, bool) or not isinstance(cutoff, int):
        raise TypeError("cutoff must be an integer")
    if cutoff < 2:
        raise ValueError("cutoff must be >= 2")
    return primes_up_to(cutoff)


def _validate_diagonal_time(n: int) -> int:
    if isinstance(n, bool) or not isinstance(n, int):
        raise TypeError("n must be an integer")
    if n < 2:
        raise ValueError("n must be >= 2")
    return n


def uncovered_measure(n: int, primes: Iterable[int] | None = None) -> Fraction:
    """Return exact ``U(n)`` as a rational number."""
    _validate_diagonal_time(n)
    prime_values = primes_up_to(n) if primes is None else [p for p in primes if p <= n]
    return diagonal_uncovered_measure_for_primes(n, prime_values)


def diagonal_uncovered_measure_for_primes(n: int, prime_values: Iterable[int]) -> Fraction:
    """Return exact diagonal-time uncovered measure for a fixed prime set."""
    _validate_diagonal_time(n)
    primes = list(prime_values)
    covered = [
        interval
        for p in primes
        for interval in split_circular_interval(diagonal_center(n, p), Fraction(1, 2 * p))
    ]
    return total_measure(complement_intervals(covered))


def residue_uncovered_measure_for_primes(n: int, prime_values: Iterable[int]) -> Fraction:
    """Return exact residue-time uncovered measure for a fixed prime set.

    This is the fixed-cutoff CRT-period helper. It accepts residue times
    ``n >= 0`` and does not impose the diagonal app-level condition ``p <= n``.
    """
    primes = list(prime_values)
    covered = [
        interval
        for p in primes
        for interval in split_circular_interval(residue_center(n, p), Fraction(1, 2 * p))
    ]
    return total_measure(complement_intervals(covered))


def uncovered_measure_for_primes(n: int, prime_values: Iterable[int]) -> Fraction:
    """Backward-compatible alias for diagonal fixed-prime uncovered measure."""
    return diagonal_uncovered_measure_for_primes(n, prime_values)


def cutoff_uncovered_measure(n: int, cutoff: int) -> Fraction:
    """Return exact ``U_x(n)`` for all primes ``p <= cutoff``."""
    return residue_uncovered_measure_for_primes(n, _prime_values_for_cutoff(cutoff))


def mertens_product_baseline(n: int, primes: Iterable[int] | None = None) -> float:
    """Return ``prod_{p <= n}(1 - 1/p)``."""
    prime_values = primes_up_to(n) if primes is None else [p for p in primes if p <= n]
    return mertens_product_for_primes(prime_values)


def mertens_product_for_primes(prime_values: Iterable[int]) -> float:
    """Return ``prod_p (1 - 1/p)`` for a fixed prime set."""
    baseline = 1.0
    for p in prime_values:
        baseline *= 1.0 - 1.0 / p
    return baseline


def cutoff_mertens_product_baseline(cutoff: int) -> float:
    """Return ``prod_{p <= cutoff}(1 - 1/p)``."""
    return mertens_product_for_primes(_prime_values_for_cutoff(cutoff))


def poisson_baseline(n: int, primes: Iterable[int] | None = None) -> float:
    """Return ``exp(-sum_{p <= n} 1/p)``."""
    prime_values = primes_up_to(n) if primes is None else [p for p in primes if p <= n]
    return math.exp(-sum(1.0 / p for p in prime_values))
