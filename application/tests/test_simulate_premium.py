"""Tests for ``SimulatePremiumUseCase``: GIS routing and delegation to ``PremiumCalculator``."""

from decimal import Decimal

from application.dto.simulation_inputs import SimulationInputs
from application.use_cases.simulate_premium import SimulatePremiumUseCase
from domain.entities.car import Car
from domain.ports.gis_rate_adjustment import GisRateAdjustmentPort
from domain.services.premium_calculation import PremiumCalculationPolicy, PremiumCalculator
from domain.value_objects.address import Address


def _calculator():
    policy = PremiumCalculationPolicy(
        base_coverage_percentage=Decimal("1"),
        rate_per_age_year=Decimal("0.005"),
        rate_per_value_chunk=Decimal("0.005"),
        value_chunk_size=Decimal("10000"),
    )
    return PremiumCalculator(policy=policy)


class _FixedGis(GisRateAdjustmentPort):
    def __init__(self, variation: Decimal) -> None:
        self._variation = variation

    def rate_variation_for_address(self, address: Address) -> Decimal:
        return self._variation


class _SpyGis(GisRateAdjustmentPort):
    def __init__(self) -> None:
        self.call_count = 0

    def rate_variation_for_address(self, address: Address) -> Decimal:
        self.call_count += 1
        return Decimal("0")


def test_execute_applies_gis_when_registration_location_provided():
    car = Car(make="Toyota", model="Corolla", value=Decimal("100000"), year=2016)
    use_case = SimulatePremiumUseCase(
        calculator=_calculator(),
        gis_rate_adjustment=_FixedGis(Decimal("0.01")),
    )
    addr = Address(city="Lisbon", country="PT")
    result = use_case.execute(
        SimulationInputs(
            broker_fee=Decimal("50"),
            car=car,
            current_year=2026,
            deductible_percentage=Decimal("0.10"),
            registration_location=addr,
        ),
    )
    assert result.applied_rate == Decimal("0.11")


def test_execute_matches_readme_decade_example_without_gis():
    car = Car(make="Toyota", model="Corolla", value=Decimal("100000"), year=2016)
    use_case = SimulatePremiumUseCase(
        calculator=_calculator(),
        gis_rate_adjustment=_SpyGis(),
    )
    result = use_case.execute(
        SimulationInputs(
            broker_fee=Decimal("50"),
            car=car,
            current_year=2026,
            deductible_percentage=Decimal("0.10"),
        ),
    )
    assert result.applied_rate == Decimal("0.10")
    assert result.calculated_premium == Decimal("9050")
    assert result.deductible_value == Decimal("10000")
    assert result.policy_limit == Decimal("90000")


def test_execute_skips_gis_port_when_no_registration_location():
    spy = _SpyGis()
    car = Car(make="Ford", model="Focus", value=Decimal("10000"), year=2020)
    use_case = SimulatePremiumUseCase(
        calculator=_calculator(),
        gis_rate_adjustment=spy,
    )
    use_case.execute(
        SimulationInputs(
            broker_fee=Decimal("0"),
            car=car,
            current_year=2026,
            deductible_percentage=Decimal("0"),
        ),
    )
    assert spy.call_count == 0
