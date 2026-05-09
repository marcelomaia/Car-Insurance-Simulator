"""Premium simulation HTTP routes."""

from typing import Annotated

from fastapi import APIRouter, Depends

from application.use_cases.simulate_premium import SimulatePremiumUseCase
from presentation.deps import get_current_year, get_simulate_use_case
from presentation.mappers import simulation_inputs_from_http
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
    inputs = simulation_inputs_from_http(body, current_year)
    calculated = use_case.execute(inputs)
    return premium_simulation_response_from_calculated(calculated)
