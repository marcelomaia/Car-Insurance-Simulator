"""Extra scenarios for ``SimulatePremiumUseCase`` (GIS extremes, deductibles, spy guarantees)."""

from decimal import Decimal

import pytest

from application.dto.simulation_inputs import SimulationInputs
from application.use_cases.simulate_premium import SimulatePremiumUseCase
from domain.entities.car import Car
from domain.exceptions import InvalidDeductiblePercentageError, NegativeAppliedRateError
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
        self.last_address: Address | None = None

    def rate_variation_for_address(self, address: Address) -> Decimal:
        self.last_address = address
        return Decimal("0")


def test_execute_passes_registration_location_to_gis_adapter():
    spy = _SpyGis()
    addr = Address(city="Porto", country="PT")
    car = Car(make="Z", model="Z", value=Decimal("1"), year=2026)
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
            registration_location=addr,
        ),
    )
    assert spy.last_address == addr


def test_execute_raises_when_applied_rate_negative_after_gis():
    car = Car(make="Mini", model="Risk", value=Decimal("0"), year=2026)
    use_case = SimulatePremiumUseCase(
        calculator=_calculator(),
        gis_rate_adjustment=_FixedGis(Decimal("-0.05")),
    )
    with pytest.raises(NegativeAppliedRateError, match="applied_rate"):
        use_case.execute(
            SimulationInputs(
                broker_fee=Decimal("0"),
                car=car,
                current_year=2026,
                deductible_percentage=Decimal("0"),
                registration_location=Address(city="X", country="Y"),
            ),
        )


def test_execute_raises_when_deductible_percentage_above_one():
    """API mistakes (e.g. ``10`` for 10% instead of ``0.10``) must fail: fraction must stay in ``[0, 1]``.

    Here ``Decimal("3")`` is deliberately absurd (300% as a fraction, or three times full coverage).
    """
    car = Car(make="A", model="B", value=Decimal("5000"), year=2024)
    use_case = SimulatePremiumUseCase(
        calculator=_calculator(),
        gis_rate_adjustment=_FixedGis(Decimal("0")),
    )
    with pytest.raises(InvalidDeductiblePercentageError, match="deductible_percentage"):
        use_case.execute(
            SimulationInputs(
                broker_fee=Decimal("0"),
                car=car,
                current_year=2026,
                deductible_percentage=Decimal("3"),
            ),
        )
