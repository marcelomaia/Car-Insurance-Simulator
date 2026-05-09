"""Premium calculation policy and orchestrator (pure domain; ``current_year`` passed in per call).

Money-like amounts and tariff coefficients use :class:`decimal.Decimal` instead of ``float``
so decimal fractions (rates, premiums, limits) stay exact under arithmetic—binary floats are
not suitable for regulated monetary semantics.
"""

from dataclasses import dataclass
from decimal import Decimal

from domain.entities.car import Car
from domain.exceptions import InvalidDeductiblePercentageError, NegativeAppliedRateError
from domain.value_objects.policy_limit_breakdown import PolicyLimitBreakdown
from domain.value_objects.premium_breakdown import PremiumBreakdown


def _applied_rate_non_negative_or_raise(applied_rate: Decimal) -> None:
    if applied_rate < Decimal("0"):
        msg = "applied_rate cannot be negative; combined intrinsic and GIS rate must be non-negative."
        raise NegativeAppliedRateError(msg)


def _deductible_percentage_unit_interval_or_raise(deductible_percentage: Decimal) -> None:
    if deductible_percentage < Decimal("0") or deductible_percentage > Decimal("1"):
        msg = "deductible_percentage must be between 0 and 1 inclusive (fraction of coverage/premium)."
        raise InvalidDeductiblePercentageError(msg)


@dataclass(frozen=True)
class PremiumCalculationPolicy:
    """Configurable tariff coefficients (typically loaded via settings in outer layers)."""

    base_coverage_percentage: Decimal
    rate_per_age_year: Decimal
    rate_per_value_chunk: Decimal
    value_chunk_size: Decimal


@dataclass(frozen=True)
class PremiumCalculator:
    """Encapsulates rating rules bound to a ``PremiumCalculationPolicy``."""

    policy: PremiumCalculationPolicy

    def compute_applied_rate(self, gis_rate_variation: Decimal, intrinsic_rate: Decimal) -> Decimal:
        """GIS adjustment is applied additively to the intrinsic decimal rate (e.g. +0.01 = +1%)."""
        return intrinsic_rate + gis_rate_variation

    def compute_intrinsic_rate(self, car: Car, current_year: int) -> Decimal:
        """Combine age-based and value-chunk rate contributions for ``car``."""
        age_years = max(0, current_year - car.year)
        age_component = Decimal(age_years) * self.policy.rate_per_age_year
        value_component = (car.value / self.policy.value_chunk_size) * self.policy.rate_per_value_chunk
        return age_component + value_component

    def compute_policy_limit_breakdown(self, car: Car, deductible_percentage: Decimal) -> PolicyLimitBreakdown:
        """Derive base limit, deductible monetary value, and final policy limit per product rules."""
        _deductible_percentage_unit_interval_or_raise(deductible_percentage)
        base_policy_limit = car.value * self.policy.base_coverage_percentage
        deductible_value = base_policy_limit * deductible_percentage
        policy_limit = base_policy_limit - deductible_value
        return PolicyLimitBreakdown(
            base_policy_limit=base_policy_limit,
            deductible_value=deductible_value,
            policy_limit=policy_limit,
        )

    def compute_premium_breakdown(
        self,
        applied_rate: Decimal,
        broker_fee: Decimal,
        car: Car,
        deductible_percentage: Decimal,
    ) -> PremiumBreakdown:
        """Compute base premium, deductible discount, and final premium including broker fee."""
        _applied_rate_non_negative_or_raise(applied_rate)
        _deductible_percentage_unit_interval_or_raise(deductible_percentage)
        base_premium = car.value * applied_rate
        deductible_discount = base_premium * deductible_percentage
        calculated_premium = base_premium - deductible_discount + broker_fee
        return PremiumBreakdown(
            applied_rate=applied_rate,
            base_premium=base_premium,
            calculated_premium=calculated_premium,
            deductible_discount=deductible_discount,
        )
