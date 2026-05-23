"""Complete-CRT Mertens-boundary hard endpoint helpers."""

from __future__ import annotations

from collections import Counter
from fractions import Fraction
from typing import Iterable

from .multiplicity import selected_residue


def mertens_product(primes: Iterable[int]) -> Fraction:
    """Return ``P_x = prod_{p <= x} (1 - 1/p)`` as an exact fraction."""
    value = Fraction(1)
    for p in primes:
        value *= Fraction(p - 1, p)
    return value


def hard_weight(hit: bool | int, p: int) -> Fraction:
    """Return one-prime hard-endpoint weight.

    The weight is ``(1 - 1_hit) / (1 - 1/p)``. A hit gives zero; a miss gives
    ``p/(p-1)``.
    """
    if int(bool(hit)):
        return Fraction(0)
    return Fraction(p, p - 1)


def distinct_selected_residue_count(p: int, angles: Iterable[float | Fraction]) -> int:
    """Return the number of distinct selected residues at prime ``p``."""
    return len({selected_residue(alpha, p) for alpha in angles})


def hard_q_point_local_factor(p: int, angles: Iterable[float | Fraction]) -> Fraction:
    """Return the q-point local factor for the hard uncovered endpoint."""
    angle_values = list(angles)
    q = len(angle_values)
    if q == 0:
        return Fraction(1)
    k = distinct_selected_residue_count(p, angle_values)
    return Fraction(p - k, p) * Fraction(p, p - 1) ** q


def hard_q_point_factor(primes: Iterable[int], angles: Iterable[float | Fraction]) -> Fraction:
    """Return the complete-CRT q-point hard-endpoint product factor."""
    angle_values = list(angles)
    value = Fraction(1)
    for p in primes:
        value *= hard_q_point_local_factor(p, angle_values)
    return value


def hard_two_point_local_factor(p: int, alpha: float | Fraction, gamma: float | Fraction) -> Fraction:
    """Return the two-point hard endpoint local factor."""
    return hard_q_point_local_factor(p, [alpha, gamma])


def two_point_factor_type(p: int, alpha: float | Fraction, gamma: float | Fraction) -> str:
    """Classify a two-point local factor as collision or separated."""
    if selected_residue(alpha, p) == selected_residue(gamma, p):
        return "collision"
    return "separated"


def hard_density_from_residues(
    residues: dict[int, int],
    primes: Iterable[int],
    alpha: float | Fraction,
) -> Fraction:
    """Return ``1_{D_x=0}/P_x`` for fixed CRT residues and angle."""
    prime_values = list(primes)
    for p in prime_values:
        if residues[p] == selected_residue(alpha, p):
            return Fraction(0)
    return Fraction(1, 1) / mertens_product(prime_values)


def cell_polynomial_coefficients(
    residues: dict[int, int],
    primes: Iterable[int],
) -> dict[int, Fraction]:
    """Return exact coefficients of ``int_T u^{D_x(R,alpha)} d alpha``.

    The selected residue is constant between half-open cell boundaries
    ``(2r+1)/(2p)``. The endpoint assignment is immaterial for Lebesgue
    coefficients, so each open cell is sampled at its midpoint.
    """
    prime_values = list(primes)
    boundaries = {Fraction(0), Fraction(1)}
    for p in prime_values:
        for r in range(p):
            boundaries.add(Fraction(2 * r + 1, 2 * p) % 1)
    ordered = sorted(boundaries)
    coefficients: Counter[int] = Counter()
    for left, right in zip(ordered, ordered[1:]):
        if left == right:
            continue
        midpoint = (left + right) / 2
        length = right - left
        multiplicity = sum(1 for p in prime_values if residues[p] == selected_residue(midpoint, p))
        coefficients[multiplicity] += length
    return dict(sorted(coefficients.items()))
