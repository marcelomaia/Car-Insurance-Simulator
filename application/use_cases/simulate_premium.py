"""Orchestrates premium simulation: optional GIS via port, rating delegated to ``PremiumCalculator``."""

from decimal import Decimal

from application.dto.simulation_inputs import SimulationInputs
from domain.events.premium_calculated import PremiumCalculated
from domain.ports.gis_rate_adjustment import GisRateAdjustmentPort
from domain.services.premium_calculation import PremiumCalculator


class SimulatePremiumUseCase:
    """Supplies ``current_year`` per request; domain stays clock-free."""

    def __init__(self, calculator: PremiumCalculator, gis_rate_adjustment: GisRateAdjustmentPort) -> None:
        self._calculator = calculator
        self._gis_rate_adjustment = gis_rate_adjustment

    def execute(self, inputs: SimulationInputs) -> PremiumCalculated:
        gis_rate_variation = (
            self._gis_rate_adjustment.rate_variation_for_address(inputs.registration_location)
            if inputs.registration_location is not None
            else Decimal("0")
        )
        intrinsic_rate = self._calculator.compute_intrinsic_rate(inputs.car, inputs.current_year)
        applied_rate = self._calculator.compute_applied_rate(gis_rate_variation, intrinsic_rate)
        limit_breakdown = self._calculator.compute_policy_limit_breakdown(
            inputs.car,
            inputs.deductible_percentage,
        )
        premium_breakdown = self._calculator.compute_premium_breakdown(
            applied_rate,
            inputs.broker_fee,
            inputs.car,
            inputs.deductible_percentage,
        )
        return PremiumCalculated(
            applied_rate=premium_breakdown.applied_rate,
            calculated_premium=premium_breakdown.calculated_premium,
            car=inputs.car,
            deductible_value=limit_breakdown.deductible_value,
            policy_limit=limit_breakdown.policy_limit,
        )
