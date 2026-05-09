from dataclasses import dataclass

from domain.entities.car import Car


@dataclass(frozen=True)
class PremiumCalculated:
    applied_rate: float
    calculated_premium: float
    car: Car
    deductible_value: float
    policy_limit: float
