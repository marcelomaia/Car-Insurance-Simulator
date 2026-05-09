from dataclasses import dataclass
from decimal import Decimal

from domain.entities.car import Car


@dataclass(frozen=True)
class PremiumCalculated:
    applied_rate: Decimal
    calculated_premium: Decimal
    car: Car
    deductible_value: Decimal
    policy_limit: Decimal
