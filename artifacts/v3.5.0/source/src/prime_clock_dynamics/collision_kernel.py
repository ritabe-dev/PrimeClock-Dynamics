"""Collision-kernel helpers for shrinking-angle Angular EK drafts."""

from __future__ import annotations

from fractions import Fraction
from typing import Iterable

from .multiplicity import multiplicity_covariance_baseline, selected_residue


def selected_residue_exact(alpha: float | Fraction, p: int) -> int:
    """Return the exact half-open selected residue ``r_p(alpha)``."""
    return selected_residue(alpha, p)


def collision_kernel_term(alpha: float | Fraction, beta: float | Fraction, p: int) -> Fraction:
    """Return the complete-CRT covariance contribution for one prime."""
    if selected_residue(alpha, p) == selected_residue(beta, p):
        return Fraction(1, p) * (1 - Fraction(1, p))
    return -Fraction(1, p * p)


def collision_kernel(
    primes: Iterable[int],
    alpha: float | Fraction,
    beta: float | Fraction,
) -> Fraction:
    """Return ``K_x(alpha,beta)`` for a supplied prime list."""
    return sum((collision_kernel_term(alpha, beta, p) for p in primes), Fraction(0))


def kernel_matrix(primes: Iterable[int], angles: Iterable[float | Fraction]) -> list[list[Fraction]]:
    """Return the complete-CRT covariance matrix for a finite angle list."""
    prime_values = list(primes)
    angle_values = list(angles)
    return [
        [collision_kernel(prime_values, alpha, beta) for beta in angle_values]
        for alpha in angle_values
    ]


def same_residue_prime_count(
    primes: Iterable[int],
    alpha: float | Fraction,
    beta: float | Fraction,
) -> int:
    """Return the number of primes with equal selected residues."""
    return sum(1 for p in primes if selected_residue(alpha, p) == selected_residue(beta, p))


def A_B_baseline(primes: Iterable[int]) -> tuple[Fraction, Fraction]:
    """Return the fixed-cutoff CRT mean ``A_x`` and variance ``B_x^2``."""
    prime_values = list(primes)
    mean = sum((Fraction(1, p) for p in prime_values), Fraction(0))
    variance = sum((Fraction(1, p) * (1 - Fraction(1, p)) for p in prime_values), Fraction(0))
    return mean, variance


def correlation_ratio(
    primes: Iterable[int],
    alpha: float | Fraction,
    beta: float | Fraction,
) -> float:
    """Return ``K_x(alpha,beta) / B_x^2``."""
    prime_values = list(primes)
    variance = multiplicity_covariance_baseline(alpha, alpha, prime_values)
    if variance == 0:
        raise ValueError("variance baseline is zero")
    return float(collision_kernel(prime_values, alpha, beta) / variance)
