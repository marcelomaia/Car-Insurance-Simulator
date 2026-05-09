"""Edge-case tests for ``PremiumCalculator`` (boundaries, divide-by-zero, validation).

Invalid products (deductible outside ``[0, 1]``, negative applied rate) raise domain exceptions.
"""

from decimal import Decimal, DivisionByZero

import pytest

from domain.entities.car import Car
from domain.exceptions import InvalidDeductiblePercentageError, NegativeAppliedRateError
from domain.services.premium_calculation import PremiumCalculationPolicy, PremiumCalculator


def _calculator(
    *,
    base_coverage_percentage: Decimal | None = None,
    rate_per_age_year: Decimal | None = None,
    rate_per_value_chunk: Decimal | None = None,
    value_chunk_size: Decimal | None = None,
) -> PremiumCalculator:
    policy = PremiumCalculationPolicy(
        base_coverage_percentage=(base_coverage_percentage if base_coverage_percentage is not None else Decimal("1")),
        rate_per_age_year=rate_per_age_year if rate_per_age_year is not None else Decimal("0.005"),
        rate_per_value_chunk=rate_per_value_chunk if rate_per_value_chunk is not None else Decimal("0.005"),
        value_chunk_size=value_chunk_size if value_chunk_size is not None else Decimal("10000"),
    )
    return PremiumCalculator(policy=policy)


def test_compute_applied_rate_negative_when_intrinsic_small_and_gis_negative_large():
    calculator = _calculator()
    intrinsic = Decimal("0.01")
    gis = Decimal("-0.02")
    assert calculator.compute_applied_rate(gis, intrinsic) == Decimal("-0.01")


def test_compute_intrinsic_rate_fractional_chunks_partial_second_chunk():
    calculator = _calculator()
    car = Car(make="Mini", model="One", value=Decimal("15000"), year=2026)
    intrinsic = calculator.compute_intrinsic_rate(car, 2026)
    assert intrinsic == Decimal("0.0075")


def test_compute_intrinsic_rate_large_age_and_value_accumulate_linearly():
    calculator = _calculator()
    car = Car(make="Old", model="Timer", value=Decimal("200000"), year=2000)
    intrinsic = calculator.compute_intrinsic_rate(car, 2026)
    age_part = Decimal("26") * Decimal("0.005")
    value_part = (Decimal("200000") / Decimal("10000")) * Decimal("0.005")
    assert intrinsic == age_part + value_part


def test_compute_intrinsic_rate_raises_division_by_zero_when_value_chunk_size_zero():
    calculator = _calculator(value_chunk_size=Decimal("0"))
    car = Car(make="X", model="Y", value=Decimal("1000"), year=2020)
    with pytest.raises(DivisionByZero):
        calculator.compute_intrinsic_rate(car, 2026)


def test_compute_intrinsic_rate_same_calendar_year_as_car_year_yields_zero_age_component():
    calculator = _calculator()
    car = Car(make="New", model="Car", value=Decimal("30000"), year=2026)
    intrinsic = calculator.compute_intrinsic_rate(car, 2026)
    assert intrinsic == (Decimal("30000") / Decimal("10000")) * Decimal("0.005")


def test_compute_intrinsic_rate_zero_car_value_nonzero_age():
    calculator = _calculator()
    car = Car(make="Gift", model="Car", value=Decimal("0"), year=2010)
    intrinsic = calculator.compute_intrinsic_rate(car, 2026)
    assert intrinsic == Decimal("16") * Decimal("0.005")


def test_compute_policy_limit_breakdown_full_deductible_yields_zero_final_limit():
    calculator = _calculator()
    car = Car(make="A", model="B", value=Decimal("80000"), year=2019)
    result = calculator.compute_policy_limit_breakdown(car, Decimal("1"))
    assert result.base_policy_limit == Decimal("80000")
    assert result.deductible_value == Decimal("80000")
    assert result.policy_limit == Decimal("0")


def test_compute_policy_limit_breakdown_raises_when_deductible_above_one():
    calculator = _calculator()
    car = Car(make="A", model="B", value=Decimal("50000"), year=2018)
    with pytest.raises(InvalidDeductiblePercentageError, match="deductible_percentage"):
        calculator.compute_policy_limit_breakdown(car, Decimal("1.5"))


def test_compute_policy_limit_breakdown_raises_when_deductible_negative():
    calculator = _calculator()
    car = Car(make="A", model="B", value=Decimal("10000"), year=2020)
    with pytest.raises(InvalidDeductiblePercentageError, match="deductible_percentage"):
        calculator.compute_policy_limit_breakdown(car, Decimal("-0.05"))


def test_compute_policy_limit_breakdown_zero_deductible_equals_base():
    calculator = _calculator()
    car = Car(make="A", model="B", value=Decimal("40000"), year=2021)
    result = calculator.compute_policy_limit_breakdown(car, Decimal("0"))
    assert result.base_policy_limit == Decimal("40000")
    assert result.deductible_value == Decimal("0")
    assert result.policy_limit == Decimal("40000")


def test_compute_premium_breakdown_raises_when_applied_rate_negative():
    calculator = _calculator()
    car = Car(make="A", model="B", value=Decimal("10000"), year=2022)
    with pytest.raises(NegativeAppliedRateError, match="applied_rate"):
        calculator.compute_premium_breakdown(
            Decimal("-0.01"),
            Decimal("0"),
            car,
            Decimal("0.10"),
        )


def test_compute_premium_breakdown_raises_when_deductible_above_one():
    calculator = _calculator()
    car = Car(make="A", model="B", value=Decimal("10000"), year=2022)
    with pytest.raises(InvalidDeductiblePercentageError, match="deductible_percentage"):
        calculator.compute_premium_breakdown(
            Decimal("0.10"),
            Decimal("0"),
            car,
            Decimal("2"),
        )


def test_compute_premium_breakdown_zero_broker_zero_deductible():
    calculator = _calculator()
    car = Car(make="A", model="B", value=Decimal("20000"), year=2023)
    breakdown = calculator.compute_premium_breakdown(
        Decimal("0.05"),
        Decimal("0"),
        car,
        Decimal("0"),
    )
    assert breakdown.calculated_premium == Decimal("1000")


def test_compute_premium_breakdown_zero_car_value_positive_rate_yields_zero_premium():
    calculator = _calculator()
    car = Car(make="Zero", model="Value", value=Decimal("0"), year=2015)
    breakdown = calculator.compute_premium_breakdown(
        Decimal("0.10"),
        Decimal("25"),
        car,
        Decimal("0.05"),
    )
    assert breakdown.base_premium == Decimal("0")
    assert breakdown.calculated_premium == Decimal("25")
