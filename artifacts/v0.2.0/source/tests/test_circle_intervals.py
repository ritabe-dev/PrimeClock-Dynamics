from fractions import Fraction

from prime_clock_dynamics.circle import CircularInterval, contains_angle
from prime_clock_dynamics.intervals import (
    complement_intervals,
    merge_intervals,
    split_circular_interval,
    total_measure,
)


def test_half_open_membership_excludes_right_endpoint() -> None:
    interval = CircularInterval(center=Fraction(0), radius=Fraction(1, 4))
    assert contains_angle(interval, Fraction(-1, 4))
    assert contains_angle(interval, Fraction(0))
    assert not contains_angle(interval, Fraction(1, 4))


def test_wraparound_interval_split() -> None:
    assert split_circular_interval(Fraction(0), Fraction(1, 6)) == [
        (Fraction(0), Fraction(1, 6)),
        (Fraction(5, 6), Fraction(1)),
    ]


def test_merge_and_complement_exact_intervals() -> None:
    covered = merge_intervals(
        [
            (Fraction(0), Fraction(1, 4)),
            (Fraction(1, 4), Fraction(1, 2)),
            (Fraction(3, 4), Fraction(1)),
        ]
    )
    assert covered == [(Fraction(0), Fraction(1, 2)), (Fraction(3, 4), Fraction(1))]
    gaps = complement_intervals(covered)
    assert gaps == [(Fraction(1, 2), Fraction(3, 4))]
    assert total_measure(gaps) == Fraction(1, 4)
