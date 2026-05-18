from fractions import Fraction

from prime_clock_dynamics.circle import contains_angle
from prime_clock_dynamics.multiplicity import arc_for_prime, selected_residue


def test_selected_residue_matches_half_open_membership() -> None:
    angles = [
        Fraction(0),
        Fraction(1, 20),
        Fraction(1, 10),
        Fraction(1, 2),
        Fraction(9, 10),
        Fraction(19, 20),
    ]
    primes = [2, 3, 5, 7, 11]
    for p in primes:
        for alpha in angles:
            residue = selected_residue(alpha, p)
            hits = [
                n % p
                for n in range(p)
                if contains_angle(arc_for_prime(n + p, p), alpha)
            ]
            assert hits == [residue]


def test_selected_residue_endpoint_tie_goes_to_right_center() -> None:
    assert selected_residue(Fraction(1, 10), 5) == 1
    assert selected_residue(Fraction(9, 10), 5) == 0
