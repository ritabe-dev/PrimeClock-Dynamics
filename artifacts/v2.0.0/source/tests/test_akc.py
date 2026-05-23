from __future__ import annotations

from fractions import Fraction

from prime_clock_dynamics.akc import (
    crt_exponential_average,
    local_q_point_factor,
    normalizer_z,
)
from prime_clock_dynamics.primes import primes_up_to


def test_normalizer_matches_direct_complete_crt_average() -> None:
    primes = primes_up_to(7)
    beta = 0.5
    alpha = Fraction(1, 10)
    assert abs(crt_exponential_average(primes, alpha, beta) - normalizer_z(primes, beta)) < 1e-12


def test_one_point_local_factor_is_one() -> None:
    assert abs(local_q_point_factor(7, [Fraction(1, 10)], 1.0) - 1.0) < 1e-12

