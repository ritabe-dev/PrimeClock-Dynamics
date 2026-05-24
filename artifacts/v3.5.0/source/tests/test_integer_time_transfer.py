from __future__ import annotations

from prime_clock_dynamics.integer_time_transfer import (
    complete_period_average,
    complete_period_test_average,
    conductor_for_frequency,
    dyadic_average,
    dyadic_residue_total_variation,
    dyadic_residue_total_variation_formula,
    dyadic_test_average,
    moment_transfer_bound,
    normalized_uncovered_mass,
    periodic_transfer_bound,
    primorial,
    total_variation_expectation_bound,
    transfer_budget,
)
from prime_clock_dynamics.primes import primes_up_to


def test_primorial_and_budget() -> None:
    assert primorial([2, 3, 5]) == 30
    budget = transfer_budget(7, 840)
    assert budget.primorial == 210
    assert 0.0 < budget.mertens_product < 1.0
    assert budget.first_moment_ratio < 1.0


def test_complete_period_first_moment_is_one_for_small_cutoff() -> None:
    assert abs(complete_period_average(5, power=1) - 1.0) < 1e-12


def test_dyadic_error_respects_periodic_bound() -> None:
    dyadic = dyadic_average(240, 5, power=1)
    period = complete_period_average(5, power=1)
    assert abs(dyadic - period) <= periodic_transfer_bound(5, 240, power=1)


def test_total_variation_residue_bound() -> None:
    budget = transfer_budget(7, 840)
    tv_distance = dyadic_residue_total_variation(840, budget.primorial)
    assert tv_distance <= budget.primorial / budget.dyadic_n
    assert abs(tv_distance - dyadic_residue_total_variation_formula(840, budget.primorial)) < 1e-12


def test_bounded_test_transfer_bound() -> None:
    def test_fn(value: float) -> float:
        return 1.0 if value > 1.0 else 0.0

    dyadic = dyadic_test_average(840, 7, test_fn)
    period = complete_period_test_average(7, test_fn)
    bound = total_variation_expectation_bound(transfer_budget(7, 840).primorial, 840)
    assert abs(dyadic - period) <= bound


def test_moment_transfer_bound_matches_periodic_bound() -> None:
    assert moment_transfer_bound(7, 840, moment=3) == periodic_transfer_bound(7, 840, power=3)


def test_normalized_uncovered_mass_is_nonnegative() -> None:
    for n in range(1, 20):
        assert normalized_uncovered_mass(n, 5) >= 0.0


def test_conductor_for_frequency() -> None:
    period = primorial(primes_up_to(5))
    assert period == 30
    assert conductor_for_frequency(period, 0) == 1
    assert conductor_for_frequency(period, 1) == 30
    assert conductor_for_frequency(period, 10) == 3
