"""Tests for ``PremiumCalculator`` numeric rules.

Premiums, limits, and rates use :class:`decimal.Decimal` in the domain so amounts match
decimal arithmetic (unlike binary ``float``). Assertions compare ``Decimal`` values built
from string literals—exact equality is reliable here.
"""

from decimal import Decimal

from domain.entities.car import Car
from domain.services.premium_calculation import PremiumCalculationPolicy, PremiumCalculator


def _calculator():
    policy = PremiumCalculationPolicy(
        base_coverage_percentage=Decimal("1"),
        rate_per_age_year=Decimal("0.005"),
        rate_per_value_chunk=Decimal("0.005"),
        value_chunk_size=Decimal("10000"),
    )
    return PremiumCalculator(policy=policy)


def test_compute_applied_rate_adds_gis_variation():
    calculator = _calculator()
    assert calculator.compute_applied_rate(Decimal("0.01"), Decimal("0.10")) == Decimal("0.11")


def test_compute_intrinsic_rate_matches_readme_decade_example():
    calculator = _calculator()
    car = Car(make="Toyota", model="Corolla", value=Decimal("100000"), year=2016)
    intrinsic = calculator.compute_intrinsic_rate(car, 2026)
    assert intrinsic == Decimal("0.10")


def test_compute_intrinsic_rate_zero_age_when_vehicle_year_is_future():
    calculator = _calculator()
    car = Car(make="Ford", model="Focus", value=Decimal("50000"), year=2030)
    intrinsic = calculator.compute_intrinsic_rate(car, 2020)
    assert intrinsic == Decimal("0.025")


def test_compute_policy_limit_breakdown_deductible_and_final():
    calculator = _calculator()
    car = Car(make="Honda", model="Civic", value=Decimal("100000"), year=2018)
    result = calculator.compute_policy_limit_breakdown(car, Decimal("0.10"))
    assert result.base_policy_limit == Decimal("100000")
    assert result.deductible_value == Decimal("10000")
    assert result.policy_limit == Decimal("90000")


def test_compute_premium_breakdown_final_premium_formula():
    calculator = _calculator()
    car = Car(make="VW", model="Golf", value=Decimal("100000"), year=2015)
    breakdown = calculator.compute_premium_breakdown(
        Decimal("0.10"),
        Decimal("50"),
        car,
        Decimal("0.10"),
    )
    assert breakdown.base_premium == Decimal("10000")
    assert breakdown.deductible_discount == Decimal("1000")
    assert breakdown.calculated_premium == Decimal("9050")
