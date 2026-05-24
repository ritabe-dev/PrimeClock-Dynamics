"""Prime Clock Multiplicity Field."""

from __future__ import annotations

from fractions import Fraction
from typing import Iterable

from .circle import CircularInterval, contains_angle
from .primes import primes_up_to


def _validate_n(n: int) -> int:
    if isinstance(n, bool) or not isinstance(n, int):
        raise TypeError("n must be an integer")
    if n < 2:
        raise ValueError("n must be >= 2")
    return n


def _validate_residue_time(n: int) -> int:
    if isinstance(n, bool) or not isinstance(n, int):
        raise TypeError("n must be an integer")
    if n < 0:
        raise ValueError("n must be nonnegative")
    return n


def _validate_prime_index(p: int) -> int:
    if isinstance(p, bool) or not isinstance(p, int):
        raise TypeError("p must be an integer")
    if p <= 0:
        raise ValueError("p must be positive")
    return p


def residue_center(n: int, p: int) -> Fraction:
    """Return ``(n mod p) / p`` for fixed-cutoff residue-time models."""
    _validate_residue_time(n)
    _validate_prime_index(p)
    return Fraction(n % p, p)


def diagonal_center(n: int, p: int) -> Fraction:
    """Return ``(n mod p) / p`` for the diagonal app-level model."""
    _validate_n(n)
    return residue_center(n, p)


def center(n: int, p: int) -> Fraction:
    """Return ``c_p(n) = (n mod p)/p`` for the diagonal model."""
    return diagonal_center(n, p)


def selected_residue(alpha: float | Fraction, p: int) -> int:
    """Return the residue selected by ``alpha`` for prime-indexed arcs.

    This follows the repository's half-open point-membership convention:
    the arc centered at ``r / p`` covers
    ``[r / p - 1/(2p), r / p + 1/(2p))`` on ``R/Z``.
    """
    _validate_prime_index(p)
    point = Fraction(alpha) % 1
    return int((p * point + Fraction(1, 2)) // 1) % p


def cutoff_multiplicity(n: int, alpha: float | Fraction, primes: Iterable[int]) -> int:
    """Return fixed-prime cutoff multiplicity ``D_x(n, alpha)``.

    Unlike ``multiplicity``, this helper does not filter primes by ``p <= n``.
    It is intended for fixed-cutoff CRT-period calculations.
    """
    n = _validate_residue_time(n)
    return sum(1 for p in primes if n % p == selected_residue(alpha, p))


def multiplicity_moment_baseline(primes: Iterable[int]) -> tuple[Fraction, Fraction]:
    """Return exact CRT-period mean and variance for fixed-prime ``D_x``."""
    mean = Fraction(0)
    variance = Fraction(0)
    for p in primes:
        selected_residue(0, p)
        mean += Fraction(1, p)
        variance += Fraction(1, p) * (1 - Fraction(1, p))
    return mean, variance


def multiplicity_covariance_baseline(
    alpha: float | Fraction,
    beta: float | Fraction,
    primes: Iterable[int],
) -> Fraction:
    """Return exact CRT-period covariance for two fixed-angle cutoff fields."""
    covariance = Fraction(0)
    for p in primes:
        alpha_residue = selected_residue(alpha, p)
        beta_residue = selected_residue(beta, p)
        if alpha_residue == beta_residue:
            covariance += Fraction(1, p) * (1 - Fraction(1, p))
        else:
            covariance -= Fraction(1, p * p)
    return covariance


def arc_for_prime(n: int, p: int) -> CircularInterval:
    """Return the prime-indexed arc for ``p`` at integer time ``n``."""
    return CircularInterval(center=diagonal_center(n, p), radius=Fraction(1, 2 * p))


def interval(n: int, p: int) -> CircularInterval:
    """Alias for ``arc_for_prime``."""
    return arc_for_prime(n, p)


def multiplicity(n: int, alpha: float | Fraction, primes: Iterable[int] | None = None) -> int:
    """Return ``D(n, alpha)`` with half-open point membership."""
    n = _validate_n(n)
    prime_values = primes_up_to(n) if primes is None else [p for p in primes if p <= n]
    if Fraction(alpha) % 1 == 0:
        return sum(1 for p in prime_values if n % p == 0)
    return sum(1 for p in prime_values if contains_angle(arc_for_prime(n, p), alpha))
