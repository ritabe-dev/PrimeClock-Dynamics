from prime_clock_dynamics.circle import contains_angle
from prime_clock_dynamics.multiplicity import arc_for_prime, multiplicity
from prime_clock_dynamics.primes import omega, primes_up_to


def test_twelve_oclock_multiplicity_equals_omega_through_10000() -> None:
    prime_pool = primes_up_to(10000)
    for n in range(2, 10001):
        assert multiplicity(n, 0, primes=prime_pool) == omega(n)


def test_zero_angle_geometric_membership_matches_divisibility() -> None:
    for n in range(2, 1000):
        for prime in primes_up_to(n):
            assert contains_angle(arc_for_prime(n, prime), 0) == (n % prime == 0)
