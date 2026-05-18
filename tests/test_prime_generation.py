from prime_clock_dynamics.primes import is_prime, omega, primes_up_to


def test_is_prime_edges() -> None:
    assert not is_prime(0)
    assert not is_prime(1)
    assert is_prime(2)
    assert is_prime(3)
    assert not is_prime(4)
    assert is_prime(97)
    assert not is_prime(99)


def test_primes_up_to() -> None:
    assert primes_up_to(1) == []
    assert primes_up_to(2) == [2]
    assert primes_up_to(20) == [2, 3, 5, 7, 11, 13, 17, 19]


def test_omega_counts_distinct_prime_divisors() -> None:
    assert omega(1) == 0
    assert omega(2) == 1
    assert omega(12) == 2
    assert omega(2 * 3 * 5 * 7) == 4
    assert omega(2**8 * 3**3 * 11) == 3
