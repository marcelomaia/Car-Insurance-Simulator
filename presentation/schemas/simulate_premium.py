"""HTTP IO models for premium simulation (PRD field names; numeric JSON as float per readme)."""

from pydantic import BaseModel, Field

from domain.events.premium_calculated import PremiumCalculated


class AddressSchema(BaseModel):
    """Optional registration location (maps to ``domain.value_objects.address.Address``)."""

    city: str
    country: str
    postal_code: str | None = None
    street: str | None = None


class PremiumSimulationRequest(BaseModel):
    """PRD input fields; fractional deductible is validated in domain (readme §5)."""

    broker_fee: float = Field(ge=0)
    deductible_percentage: float = Field(ge=0)
    make: str
    model: str
    registration_location: AddressSchema | None = None
    value: float = Field(ge=0)
    year: int


class PremiumSimulationResponse(BaseModel):
    """PRD output fields (rates and amounts as JSON floats)."""

    applied_rate: float
    calculated_premium: float
    deductible_value: float
    make: str
    model: str
    policy_limit: float
    value: float
    year: int


def premium_simulation_response_from_calculated(event: PremiumCalculated) -> PremiumSimulationResponse:
    """Map ``PremiumCalculated`` to response floats."""
    car = event.car
    return PremiumSimulationResponse(
        applied_rate=float(event.applied_rate),
        calculated_premium=float(event.calculated_premium),
        deductible_value=float(event.deductible_value),
        make=car.make,
        model=car.model,
        policy_limit=float(event.policy_limit),
        value=float(car.value),
        year=car.year,
    )
