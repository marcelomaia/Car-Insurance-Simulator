from dataclasses import dataclass


@dataclass(frozen=True)
class PolicyLimitBreakdown:
    base_policy_limit: float
    deductible_value: float
    policy_limit: float
