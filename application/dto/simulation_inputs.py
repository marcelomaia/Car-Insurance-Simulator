"""Application-level input bundle for premium simulation (framework-agnostic)."""

from dataclasses import dataclass
from decimal import Decimal

from domain.entities.car import Car
from domain.value_objects.address import Address


@dataclass(frozen=True)
class SimulationInputs:
    """All parameters needed to run ``SimulatePremiumUseCase`` (built outside the HTTP layer)."""

    broker_fee: Decimal
    car: Car
    current_year: int
    deductible_percentage: Decimal
    registration_location: Address | None = None
