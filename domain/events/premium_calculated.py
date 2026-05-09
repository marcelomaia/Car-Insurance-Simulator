from dataclasses import dataclass


@dataclass(frozen=True)
class PremiumCalculated:
    applied_rate: float
    calculated_premium: float
    deductible_value: float
    make: str
    model: str
    policy_limit: float
    value: float
    year: int
