"""Map HTTP schemas to application DTOs (presentation adapts IO; use case stays framework-free)."""

from decimal import Decimal

from application.dto.simulation_inputs import SimulationInputs
from domain.entities.car import Car
from domain.value_objects.address import Address
from presentation.schemas.simulate_premium import PremiumSimulationRequest


def simulation_inputs_from_http(body: PremiumSimulationRequest, current_year: int) -> SimulationInputs:
    """Build ``SimulationInputs`` from an API body and resolved calendar year."""
    registration_location = None
    if body.registration_location is not None:
        loc = body.registration_location
        registration_location = Address(
            city=loc.city,
            country=loc.country,
            postal_code=loc.postal_code,
            street=loc.street,
        )
    car = Car(
        make=body.make,
        model=body.model,
        value=Decimal(str(body.value)),
        year=body.year,
    )
    return SimulationInputs(
        broker_fee=Decimal(str(body.broker_fee)),
        car=car,
        current_year=current_year,
        deductible_percentage=Decimal(str(body.deductible_percentage)),
        registration_location=registration_location,
    )
