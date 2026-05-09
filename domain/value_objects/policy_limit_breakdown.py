from dataclasses import dataclass
from decimal import Decimal


@dataclass(frozen=True)
class PolicyLimitBreakdown:
    base_policy_limit: Decimal
    deductible_value: Decimal
    policy_limit: Decimal
