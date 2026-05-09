from dataclasses import dataclass


@dataclass(frozen=True)
class PremiumBreakdown:
    applied_rate: float
    base_premium: float
    calculated_premium: float
    deductible_discount: float
