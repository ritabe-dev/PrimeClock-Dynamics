"""Circle helpers on ``T = R/Z``."""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from typing import Union

Number = Union[float, Fraction]


@dataclass(frozen=True)
class CircularInterval:
    """A circular interval represented by center and half-width on ``R/Z``."""

    center: Fraction
    radius: Fraction

    @property
    def width(self) -> Fraction:
        return 2 * self.radius


def mod1(value: Number) -> Number:
    """Return ``value mod 1`` in ``[0, 1)``."""
    return value % 1


def circle_distance(left: Number, right: Number) -> Number:
    """Return the shortest circular distance between two normalized points."""
    delta = abs(mod1(left) - mod1(right))
    return min(delta, 1 - delta)


def contains_angle(interval: CircularInterval, alpha: Number) -> bool:
    """Return whether ``alpha`` is in ``interval`` using half-open membership.

    The left endpoint is included and the right endpoint is excluded in a local
    coordinate centered at the interval center. This avoids endpoint
    double-counting at ``alpha = 0`` and makes ``D(n,0)=omega(n)`` exact.
    """
    if interval.radius < 0:
        raise ValueError("interval radius must be nonnegative")
    if interval.width >= 1:
        return True

    point = Fraction(alpha) % 1
    center = interval.center % 1
    offset = (point - center + Fraction(1, 2)) % 1 - Fraction(1, 2)
    return -interval.radius <= offset < interval.radius
