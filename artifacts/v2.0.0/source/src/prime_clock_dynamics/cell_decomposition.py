"""Exact angular cell-decomposition helpers for AKC audits."""

from __future__ import annotations

from fractions import Fraction
import math
from typing import Iterable, Union

from .akc import normalizer_z
from .intervals import split_circular_interval, total_measure
from .multiplicity import residue_center, selected_residue


ResidueSource = Union[int, dict[int, int]]


def _residue_for(source: ResidueSource, p: int) -> int:
    if isinstance(source, dict):
        return source[p] % p
    return source % p


def _arcs_for_residues(source: ResidueSource, primes: Iterable[int]) -> list[tuple[Fraction, Fraction]]:
    arcs: list[tuple[Fraction, Fraction]] = []
    for p in primes:
        center = Fraction(_residue_for(source, p), p)
        radius = Fraction(1, 2 * p)
        arcs.extend(split_circular_interval(center, radius))
    return arcs


def arc_endpoints_for_residues(residues: ResidueSource, primes: Iterable[int]) -> list[Fraction]:
    """Return sorted endpoints of fixed-cutoff arcs for an integer or CRT residues."""
    endpoints: set[Fraction] = set()
    for p in primes:
        center = residue_center(residues, p) if isinstance(residues, int) else Fraction(residues[p] % p, p)
        radius = Fraction(1, 2 * p)
        for start, end in split_circular_interval(center, radius):
            endpoints.add(start % 1)
            endpoints.add(end % 1)
    return sorted(endpoints)


def cell_decomposition(endpoints: Iterable[Fraction]) -> list[tuple[Fraction, Fraction]]:
    """Return half-open cells induced by circular endpoints."""
    points = sorted({point % 1 for point in endpoints})
    if not points:
        return [(Fraction(0), Fraction(1))]
    cells: list[tuple[Fraction, Fraction]] = []
    for index, start in enumerate(points):
        end = points[(index + 1) % len(points)]
        if index == len(points) - 1:
            cells.append((start, end + 1))
        elif start != end:
            cells.append((start, end))
    return cells


def _cell_midpoint(cell: tuple[Fraction, Fraction]) -> Fraction:
    start, end = cell
    return ((start + end) / 2) % 1


def _multiplicity_at(source: ResidueSource, primes: Iterable[int], alpha: Fraction) -> int:
    return sum(1 for p in primes if _residue_for(source, p) == selected_residue(alpha, p))


def sweep_multiplicity(
    cells: Iterable[tuple[Fraction, Fraction]],
    arcs: Iterable[tuple[Fraction, Fraction]],
) -> list[dict[str, Fraction | int]]:
    """Return cell lengths and multiplicities for normalized split arcs."""
    arc_values = list(arcs)
    rows: list[dict[str, Fraction | int]] = []
    for start, end in cells:
        midpoint = _cell_midpoint((start, end))
        multiplicity = sum(1 for arc_start, arc_end in arc_values if arc_start <= midpoint < arc_end)
        rows.append(
            {
                "start": start % 1,
                "end": end % 1,
                "length": end - start,
                "multiplicity": multiplicity,
            }
        )
    return rows


def exact_mu_total(residues: ResidueSource, primes: Iterable[int], beta: float) -> float:
    """Compute exact total AKC mass by integrating over angular cells."""
    prime_values = list(primes)
    cells = cell_decomposition(arc_endpoints_for_residues(residues, prime_values))
    z_value = normalizer_z(prime_values, beta)
    total = 0.0
    for cell in cells:
        midpoint = _cell_midpoint(cell)
        multiplicity = _multiplicity_at(residues, prime_values, midpoint)
        total += float(cell[1] - cell[0]) * math.exp(beta * multiplicity) / z_value
    return total


def exact_uncovered_measure(residues: ResidueSource, primes: Iterable[int]) -> Fraction:
    """Return exact measure of angles uncovered by all fixed-cutoff arcs."""
    from .intervals import complement_intervals

    return total_measure(complement_intervals(_arcs_for_residues(residues, primes)))


def exact_high_points(residues: ResidueSource, primes: Iterable[int]) -> dict[str, object]:
    """Return exact high-point summary from the cell decomposition."""
    prime_values = list(primes)
    cells = cell_decomposition(arc_endpoints_for_residues(residues, prime_values))
    rows = []
    max_multiplicity = -1
    for start, end in cells:
        midpoint = _cell_midpoint((start, end))
        multiplicity = _multiplicity_at(residues, prime_values, midpoint)
        row = {"start": start, "end": end % 1, "length": end - start, "multiplicity": multiplicity}
        rows.append(row)
        max_multiplicity = max(max_multiplicity, multiplicity)
    argmax_cells = [row for row in rows if row["multiplicity"] == max_multiplicity]
    return {
        "max_multiplicity": max_multiplicity,
        "argmax_total_length": sum((row["length"] for row in argmax_cells), Fraction(0)),
        "cell_count": len(rows),
        "argmax_cells": argmax_cells,
    }
