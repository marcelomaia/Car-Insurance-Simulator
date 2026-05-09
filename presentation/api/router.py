"""Premium simulation HTTP routes."""

from decimal import Decimal
from typing import Annotated

from fastapi import APIRouter, Depends

from application.use_cases.simulate_premium import SimulatePremiumUseCase
from domain.entities.car import Car
from domain.value_objects.address import Address
from presentation.deps import get_current_year, get_simulate_use_case
from presentation.schemas.simulate_premium import (
    PremiumSimulationRequest,
    PremiumSimulationResponse,
    premium_simulation_response_from_calculated,
)

router = APIRouter(prefix="/v1", tags=["premium"])


@router.post("/premium/simulate", response_model=PremiumSimulationResponse)
def simulate_premium(
    body: PremiumSimulationRequest,
    current_year: Annotated[int, Depends(get_current_year)],
    use_case: Annotated[SimulatePremiumUseCase, Depends(get_simulate_use_case)],
) -> PremiumSimulationResponse:
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
    calculated = use_case.execute(
        broker_fee=Decimal(str(body.broker_fee)),
        car=car,
        current_year=current_year,
        deductible_percentage=Decimal(str(body.deductible_percentage)),
        registration_location=registration_location,
    )
    return premium_simulation_response_from_calculated(calculated)
