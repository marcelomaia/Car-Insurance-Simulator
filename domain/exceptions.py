"""Domain-specific failures (invalid tariffs or impossible product combinations)."""


class DomainError(Exception):
    """Base class for violations of domain rules and invariants."""


class InvalidDeductiblePercentageError(DomainError):
    """Raised when ``deductible_percentage`` is outside ``[0, 1]`` (fractional share)."""


class NegativeAppliedRateError(DomainError):
    """Raised when combined intrinsic + GIS rate is negative (premium would be meaningless)."""
