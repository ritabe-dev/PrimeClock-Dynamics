"""Angular Kubilius Chaos finite-beta complete-CRT helpers."""

from __future__ import annotations

from collections import Counter
from fractions import Fraction
import math
from typing import Iterable

from .multiplicity import cutoff_multiplicity, selected_residue


def normalizer_z(primes: Iterable[int], beta: float) -> float:
    """Return ``Z_x(beta)=prod_p (1+(exp(beta)-1)/p)``."""
    a_beta = math.exp(beta) - 1.0
    value = 1.0
    for p in primes:
        value *= 1.0 + a_beta / p
    return value


def normalizer_Z(primes: Iterable[int], beta: float) -> float:
    """Compatibility alias for the plan-level ``Z_x(beta)`` notation."""
    return normalizer_z(primes, beta)


def local_weight(hit: bool | int, beta: float, p: int) -> float:
    """Return one-prime normalized AKC weight for a hit indicator."""
    denominator = 1.0 + (math.exp(beta) - 1.0) / p
    return math.exp(beta * int(bool(hit))) / denominator


def sample_crt_residues(primes: Iterable[int], rng) -> dict[int, int]:
    """Sample independent complete-CRT residues ``R_p`` for supplied primes."""
    return {p: rng.randrange(p) for p in primes}


def D_from_residues(residues: dict[int, int], alpha: float | Fraction) -> int:
    """Return ``sum_p 1_{R_p=r_p(alpha)}`` from sampled CRT residues."""
    return sum(1 for p, residue in residues.items() if residue == selected_residue(alpha, p))


def mu_total_grid(
    residues: dict[int, int],
    primes: Iterable[int],
    beta: float,
    grid_size: int,
) -> float:
    """Approximate total AKC mass by a uniform angular grid."""
    if grid_size <= 0:
        raise ValueError("grid_size must be positive")
    prime_values = list(primes)
    z_value = normalizer_z(prime_values, beta)
    total = 0.0
    for index in range(grid_size):
        alpha = Fraction(index, grid_size)
        total += math.exp(beta * D_from_residues({p: residues[p] for p in prime_values}, alpha)) / z_value
    return total / grid_size


def mu_test_function_grid(
    residues: dict[int, int],
    primes: Iterable[int],
    beta: float,
    f,
    grid_size: int = 512,
) -> float:
    """Approximate ``int f(alpha) mu_{x,beta}(d alpha)`` by a grid."""
    if grid_size <= 0:
        raise ValueError("grid_size must be positive")
    prime_values = list(primes)
    z_value = normalizer_z(prime_values, beta)
    total = 0.0
    for index in range(grid_size):
        alpha = Fraction(index, grid_size)
        density = math.exp(beta * D_from_residues({p: residues[p] for p in prime_values}, alpha)) / z_value
        total += float(f(alpha)) * density
    return total / grid_size


def normalized_density(multiplicity: int, beta: float, z_value: float) -> float:
    """Return ``exp(beta * multiplicity) / Z_x(beta)``."""
    if z_value <= 0:
        raise ValueError("z_value must be positive")
    return math.exp(beta * multiplicity) / z_value


def crt_exponential_average(
    primes: Iterable[int],
    alpha: float | Fraction,
    beta: float,
) -> float:
    """Enumerate a small complete-CRT period and average ``exp(beta D_x)``."""
    prime_values = list(primes)
    period = math.prod(prime_values)
    if period > 200_000:
        raise ValueError("complete CRT enumeration would be too large")
    total = 0.0
    for n in range(period):
        total += math.exp(beta * cutoff_multiplicity(n, alpha, prime_values))
    return total / period


def local_q_point_factor(
    p: int,
    angles: Iterable[float | Fraction],
    beta: float,
) -> float:
    """Return one-prime local factor for a q-point beta moment."""
    angle_values = list(angles)
    residue_counts = Counter(selected_residue(alpha, p) for alpha in angle_values)
    numerator = 0.0
    for residue in range(p):
        numerator += math.exp(beta * residue_counts.get(residue, 0))
    numerator /= p
    denominator = (1.0 + (math.exp(beta) - 1.0) / p) ** len(angle_values)
    return numerator / denominator


def q_point_moment_factor(
    primes: Iterable[int],
    angles: Iterable[float | Fraction],
    beta: float,
) -> float:
    """Return complete-CRT normalized q-point density moment product."""
    angle_values = list(angles)
    value = 1.0
    for p in primes:
        value *= local_q_point_factor(p, angle_values, beta)
    return value
