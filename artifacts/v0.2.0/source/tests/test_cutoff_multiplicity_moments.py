from fractions import Fraction

from prime_clock_dynamics.multiplicity import (
    cutoff_multiplicity,
    multiplicity_covariance_baseline,
    multiplicity_moment_baseline,
)


def product(values: list[int]) -> int:
    result = 1
    for value in values:
        result *= value
    return result


def test_cutoff_multiplicity_crt_period_moments_match_baseline() -> None:
    primes = [2, 3, 5, 7]
    period = product(primes)
    expected_mean, expected_variance = multiplicity_moment_baseline(primes)

    for alpha in [Fraction(0), Fraction(1, 10), Fraction(1, 3), Fraction(9, 10)]:
        values = [Fraction(cutoff_multiplicity(n, alpha, primes)) for n in range(period)]
        mean = sum(values, Fraction(0)) / period
        variance = sum((value - mean) ** 2 for value in values) / period
        assert mean == expected_mean
        assert variance == expected_variance


def test_cutoff_multiplicity_zero_angle_is_cutoff_omega() -> None:
    primes = [2, 3, 5, 7, 11]
    for n in range(0, 231):
        assert cutoff_multiplicity(n, 0, primes) == sum(1 for p in primes if n % p == 0)


def test_cutoff_multiplicity_crt_period_covariance_matches_baseline() -> None:
    primes = [2, 3, 5, 7]
    period = product(primes)

    angle_pairs = [
        (Fraction(0), Fraction(0)),
        (Fraction(0), Fraction(1, 10)),
        (Fraction(1, 10), Fraction(1, 3)),
        (Fraction(1, 3), Fraction(9, 10)),
    ]
    for alpha, beta in angle_pairs:
        alpha_values = [Fraction(cutoff_multiplicity(n, alpha, primes)) for n in range(period)]
        beta_values = [Fraction(cutoff_multiplicity(n, beta, primes)) for n in range(period)]
        alpha_mean = sum(alpha_values, Fraction(0)) / period
        beta_mean = sum(beta_values, Fraction(0)) / period
        covariance = (
            sum(
                (left - alpha_mean) * (right - beta_mean)
                for left, right in zip(alpha_values, beta_values)
            )
            / period
        )
        assert covariance == multiplicity_covariance_baseline(alpha, beta, primes)
