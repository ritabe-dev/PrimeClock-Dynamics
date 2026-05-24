"""Integer-time transfer helpers for Mertens-normalized uncovered measures."""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
import math
from typing import Callable, Iterable

from .primes import primes_up_to
from .uncovered import cutoff_uncovered_measure, mertens_product_for_primes


@dataclass(frozen=True)
class TransferBudget:
    """Periodic transfer budget for a cutoff and dyadic window."""

    cutoff_y: int
    dyadic_n: int
    primorial: int
    mertens_product: float
    inverse_mertens: float

    @property
    def first_moment_ratio(self) -> float:
        """Return ``M_y log(y) / N``."""
        return self.primorial * math.log(self.cutoff_y) / self.dyadic_n

    @property
    def second_moment_ratio(self) -> float:
        """Return ``M_y (log(y))^2 / N``."""
        log_y = math.log(self.cutoff_y)
        return self.primorial * log_y * log_y / self.dyadic_n

    def log_moment_ratio(self, moment: int) -> float:
        """Return the sufficient slow-cutoff ratio ``M_y (log y)^m / N``."""
        if moment < 1:
            raise ValueError("moment must be positive")
        return self.primorial * (math.log(self.cutoff_y) ** moment) / self.dyadic_n


def primorial(prime_values: Iterable[int]) -> int:
    """Return the product of the supplied primes."""
    value = 1
    for prime in prime_values:
        value *= prime
    return value


def transfer_budget(cutoff_y: int, dyadic_n: int) -> TransferBudget:
    """Return the slow-cutoff periodic transfer budget."""
    if cutoff_y < 2:
        raise ValueError("cutoff_y must be >= 2")
    if dyadic_n < 1:
        raise ValueError("dyadic_n must be positive")
    primes = primes_up_to(cutoff_y)
    mertens = mertens_product_for_primes(primes)
    return TransferBudget(
        cutoff_y=cutoff_y,
        dyadic_n=dyadic_n,
        primorial=primorial(primes),
        mertens_product=mertens,
        inverse_mertens=1.0 / mertens,
    )


def normalized_uncovered_mass(n: int, cutoff_y: int) -> float:
    """Return exact ``U_y(n) / P_y`` as a float."""
    primes = primes_up_to(cutoff_y)
    if not primes:
        return 1.0
    uncovered = cutoff_uncovered_measure(n, cutoff_y)
    mertens = Fraction(1, 1)
    for prime in primes:
        mertens *= Fraction(prime - 1, prime)
    return float(uncovered / mertens)


def dyadic_average(
    dyadic_n: int,
    cutoff_y: int,
    *,
    power: int = 1,
    value_fn: Callable[[int, int], float] = normalized_uncovered_mass,
) -> float:
    """Return ``(1/N) sum_{N<n<=2N} value_fn(n,y)^power``."""
    if dyadic_n < 1:
        raise ValueError("dyadic_n must be positive")
    if power < 1:
        raise ValueError("power must be positive")
    total = 0.0
    for n_value in range(dyadic_n + 1, 2 * dyadic_n + 1):
        total += value_fn(n_value, cutoff_y) ** power
    return total / dyadic_n


def complete_period_average(
    cutoff_y: int,
    *,
    power: int = 1,
    value_fn: Callable[[int, int], float] = normalized_uncovered_mass,
) -> float:
    """Return the complete CRT-period average of ``value_fn(n,y)^power``."""
    budget = transfer_budget(cutoff_y, 1)
    total = 0.0
    for residue in range(budget.primorial):
        total += value_fn(residue, cutoff_y) ** power
    return total / budget.primorial


def periodic_transfer_bound(cutoff_y: int, dyadic_n: int, *, power: int = 1) -> float:
    """Return the elementary periodic transfer bound ``2 Q B / N``."""
    budget = transfer_budget(cutoff_y, dyadic_n)
    bound = budget.inverse_mertens**power
    return 2.0 * budget.primorial * bound / dyadic_n


def dyadic_residue_counts(dyadic_n: int, modulus: int) -> list[int]:
    """Return counts of ``n mod modulus`` for ``N < n <= 2N``."""
    if dyadic_n < 1:
        raise ValueError("dyadic_n must be positive")
    if modulus < 1:
        raise ValueError("modulus must be positive")
    counts = [0] * modulus
    for n_value in range(dyadic_n + 1, 2 * dyadic_n + 1):
        counts[n_value % modulus] += 1
    return counts


def dyadic_residue_total_variation(dyadic_n: int, modulus: int) -> float:
    """Return TV distance from dyadic residues to uniform residues modulo ``Q``."""
    counts = dyadic_residue_counts(dyadic_n, modulus)
    uniform = 1.0 / modulus
    return 0.5 * sum(abs((count / dyadic_n) - uniform) for count in counts)


def dyadic_residue_total_variation_formula(dyadic_n: int, modulus: int) -> float:
    """Return the exact dyadic-residue TV value ``b(Q-b)/(NQ)``."""
    if dyadic_n < 1:
        raise ValueError("dyadic_n must be positive")
    if modulus < 1:
        raise ValueError("modulus must be positive")
    _, remainder = divmod(dyadic_n, modulus)
    return remainder * (modulus - remainder) / (dyadic_n * modulus)


def total_variation_expectation_bound(
    modulus: int,
    dyadic_n: int,
    *,
    sup_norm: float = 1.0,
) -> float:
    """Return the conservative TV expectation bound ``2 Q ||G||_inf / N``."""
    if sup_norm < 0.0:
        raise ValueError("sup_norm must be nonnegative")
    if modulus < 1:
        raise ValueError("modulus must be positive")
    if dyadic_n < 1:
        raise ValueError("dyadic_n must be positive")
    return 2.0 * modulus * sup_norm / dyadic_n


def moment_transfer_bound(cutoff_y: int, dyadic_n: int, *, moment: int) -> float:
    """Return the v3.5 moment-transfer bound ``2 M_y P_y^{-m} / N``."""
    return periodic_transfer_bound(cutoff_y, dyadic_n, power=moment)


def log_moment_budget_ratio(cutoff_y: int, dyadic_n: int, *, moment: int) -> float:
    """Return the Mertens-scale sufficient ratio ``M_y (log y)^m / N``."""
    return transfer_budget(cutoff_y, dyadic_n).log_moment_ratio(moment)


def dyadic_test_average(
    dyadic_n: int,
    cutoff_y: int,
    test_fn: Callable[[float], float],
) -> float:
    """Return the dyadic average of ``test_fn(F_y(n))``."""
    if dyadic_n < 1:
        raise ValueError("dyadic_n must be positive")
    total = 0.0
    for n_value in range(dyadic_n + 1, 2 * dyadic_n + 1):
        total += test_fn(normalized_uncovered_mass(n_value, cutoff_y))
    return total / dyadic_n


def complete_period_test_average(cutoff_y: int, test_fn: Callable[[float], float]) -> float:
    """Return the complete-period average of ``test_fn(F_y(a))``."""
    budget = transfer_budget(cutoff_y, 1)
    total = 0.0
    for residue in range(budget.primorial):
        total += test_fn(normalized_uncovered_mass(residue, cutoff_y))
    return total / budget.primorial


def conductor_for_frequency(period: int, frequency: int) -> int:
    """Return the conductor of a Fourier frequency modulo ``period``."""
    if period < 1:
        raise ValueError("period must be positive")
    return period // math.gcd(period, frequency % period)


def conductor_power_summary(cutoff_y: int, *, low_conductor_bound: int) -> dict[str, float | int]:
    """Return a deterministic small-period Fourier/conductor diagnostic.

    The diagnostic groups normalized DFT power of ``F_y(n)=U_y(n)/P_y`` by the
    conductor ``M_y/gcd(k,M_y)``. It is intentionally small-scale and is not a
    theorem claim.
    """
    period = transfer_budget(cutoff_y, 1).primorial
    values = [normalized_uncovered_mass(residue, cutoff_y) for residue in range(period)]
    mean = sum(values) / period
    centered = [value - mean for value in values]
    total_power = sum(value * value for value in centered) / period
    if total_power == 0.0:
        return {
            "cutoff_y": cutoff_y,
            "period": period,
            "low_conductor_bound": low_conductor_bound,
            "mean": mean,
            "total_centered_power": 0.0,
            "low_conductor_power": 0.0,
            "high_conductor_power": 0.0,
            "low_conductor_power_ratio": 0.0,
        }

    low_power = 0.0
    for frequency in range(1, period):
        real = 0.0
        imag = 0.0
        for index, value in enumerate(centered):
            angle = -2.0 * math.pi * frequency * index / period
            real += value * math.cos(angle)
            imag += value * math.sin(angle)
        normalized_power = (real * real + imag * imag) / (period * period)
        if conductor_for_frequency(period, frequency) <= low_conductor_bound:
            low_power += normalized_power

    high_power = max(total_power - low_power, 0.0)
    return {
        "cutoff_y": cutoff_y,
        "period": period,
        "low_conductor_bound": low_conductor_bound,
        "mean": mean,
        "total_centered_power": total_power,
        "low_conductor_power": low_power,
        "high_conductor_power": high_power,
        "low_conductor_power_ratio": low_power / total_power,
    }
