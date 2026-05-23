"""Exact rational circular interval operations."""

from __future__ import annotations

from fractions import Fraction
from typing import Iterable, Tuple

ExactInterval = Tuple[Fraction, Fraction]


def split_circular_interval(center: Fraction, radius: Fraction) -> list[ExactInterval]:
    """Split a circular interval into normalized intervals in ``[0, 1]``."""
    if radius < 0:
        raise ValueError("radius must be nonnegative")
    if 2 * radius >= 1:
        return [(Fraction(0), Fraction(1))]

    one = Fraction(1)
    start = center % one - radius
    end = center % one + radius
    if start < 0:
        return [(Fraction(0), end), (one + start, one)]
    if end > one:
        return [(Fraction(0), end - one), (start, one)]
    return [(start, end)]


def merge_intervals(intervals: Iterable[ExactInterval]) -> list[ExactInterval]:
    """Merge normalized exact intervals."""
    normalized = [(start, end) for start, end in intervals if start != end]
    if not normalized:
        return []
    for start, end in normalized:
        if start < 0 or end < 0 or start > 1 or end > 1:
            raise ValueError("intervals must be normalized to [0, 1]")
        if end < start:
            raise ValueError("interval start must be <= interval end")

    normalized.sort()
    merged: list[ExactInterval] = []
    current_start, current_end = normalized[0]
    for start, end in normalized[1:]:
        if start <= current_end:
            current_end = max(current_end, end)
        else:
            merged.append((current_start, current_end))
            current_start, current_end = start, end
    merged.append((current_start, current_end))
    if len(merged) == 1 and merged[0] == (Fraction(0), Fraction(1)):
        return [(Fraction(0), Fraction(1))]
    return merged


def complement_intervals(covered: Iterable[ExactInterval]) -> list[ExactInterval]:
    """Return exact uncovered intervals on ``T`` from normalized covered intervals."""
    merged = merge_intervals(covered)
    if not merged:
        return [(Fraction(0), Fraction(1))]
    if merged == [(Fraction(0), Fraction(1))]:
        return []

    one = Fraction(1)
    gaps: list[ExactInterval] = []
    for index, (_, end) in enumerate(merged):
        next_start = merged[(index + 1) % len(merged)][0]
        gap_start = end
        gap_end = next_start + one if index == len(merged) - 1 else next_start
        if gap_end > gap_start:
            gaps.append((gap_start % one, gap_end % one))
    return gaps


def interval_length(interval: ExactInterval) -> Fraction:
    """Return exact circular interval length."""
    start, end = interval
    if end >= start:
        return end - start
    return Fraction(1) - start + end


def total_measure(intervals: Iterable[ExactInterval]) -> Fraction:
    """Return total exact measure of circular intervals."""
    return sum((interval_length(interval) for interval in intervals), Fraction(0))
