"""Pure premium and policy-limit calculations (no clock; callers pass ``current_year``)."""

from domain.value_objects.policy_limit_breakdown import PolicyLimitBreakdown
from domain.value_objects.premium_breakdown import PremiumBreakdown


def compute_applied_rate(gis_rate_variation: float, intrinsic_rate: float) -> float:
    """GIS adjustment is applied additively to the intrinsic decimal rate (e.g. +0.01 = +1%)."""
    return intrinsic_rate + gis_rate_variation


def compute_intrinsic_rate(
    car_value: float,
    current_year: int,
    rate_per_age_year: float,
    rate_per_value_chunk: float,
    value_chunk_size: float,
    vehicle_year: int,
) -> float:
    """Combine age-based and value-chunk rate contributions using caller-supplied coefficients."""
    age_years = max(0, current_year - vehicle_year)
    age_component = age_years * rate_per_age_year
    value_component = (car_value / value_chunk_size) * rate_per_value_chunk
    return age_component + value_component


def compute_policy_limit_breakdown(
    base_coverage_percentage: float,
    car_value: float,
    deductible_percentage: float,
) -> PolicyLimitBreakdown:
    """Derive base limit, deductible monetary value, and final policy limit per product rules."""
    base_policy_limit = car_value * base_coverage_percentage
    deductible_value = base_policy_limit * deductible_percentage
    policy_limit = base_policy_limit - deductible_value
    return PolicyLimitBreakdown(
        base_policy_limit=base_policy_limit,
        deductible_value=deductible_value,
        policy_limit=policy_limit,
    )


def compute_premium_breakdown(
    applied_rate: float,
    broker_fee: float,
    car_value: float,
    deductible_percentage: float,
) -> PremiumBreakdown:
    """Compute base premium, deductible discount, and final premium including broker fee."""
    base_premium = car_value * applied_rate
    deductible_discount = base_premium * deductible_percentage
    calculated_premium = base_premium - deductible_discount + broker_fee
    return PremiumBreakdown(
        applied_rate=applied_rate,
        base_premium=base_premium,
        calculated_premium=calculated_premium,
        deductible_discount=deductible_discount,
    )
