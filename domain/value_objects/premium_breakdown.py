from dataclasses import dataclass
from decimal import Decimal


@dataclass(frozen=True)
class PremiumBreakdown:
    applied_rate: Decimal
    base_premium: Decimal
    calculated_premium: Decimal
    deductible_discount: Decimal
