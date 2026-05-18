"""Prime helpers for PrimeClock Dynamics."""

from __future__ import annotations

import math


def is_prime(value: int) -> bool:
    """Return whether ``value`` is prime."""
    if isinstance(value, bool) or not isinstance(value, int):
        raise TypeError("value must be an integer")
    if value < 2:
        return False
    if value == 2:
        return True
    if value % 2 == 0:
        return False
    limit = math.isqrt(value)
    for factor in range(3, limit + 1, 2):
        if value % factor == 0:
            return False
    return True


def primes_up_to(limit: int) -> list[int]:
    """Return all primes ``p <= limit`` using an Eratosthenes sieve."""
    if isinstance(limit, bool) or not isinstance(limit, int):
        raise TypeError("limit must be an integer")
    if limit < 2:
        return []
    sieve = bytearray(b"\x01") * (limit + 1)
    sieve[0:2] = b"\x00\x00"
    root = math.isqrt(limit)
    for value in range(2, root + 1):
        if sieve[value]:
            start = value * value
            sieve[start : limit + 1 : value] = b"\x00" * (((limit - start) // value) + 1)
    return [value for value in range(2, limit + 1) if sieve[value]]


def omega(value: int) -> int:
    """Return the number of distinct prime divisors of ``value``."""
    if isinstance(value, bool) or not isinstance(value, int):
        raise TypeError("value must be an integer")
    if value < 1:
        raise ValueError("value must be >= 1")
    remaining = value
    count = 0
    for prime in primes_up_to(math.isqrt(value)):
        if remaining % prime == 0:
            count += 1
            while remaining % prime == 0:
                remaining //= prime
        if remaining == 1:
            break
    if remaining > 1:
        count += 1
    return count
