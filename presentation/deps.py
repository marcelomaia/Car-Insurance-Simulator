"""FastAPI dependencies: settings, GIS port, use case, clock boundary for ``current_year``."""

from datetime import datetime
from typing import Annotated

from fastapi import Depends

from application.use_cases.simulate_premium import SimulatePremiumUseCase
from domain.ports.gis_rate_adjustment import GisRateAdjustmentPort
from domain.services.premium_calculation import PremiumCalculator
from infrastructure.config.settings import Settings
from infrastructure.gis.mock_gis_service import MockGisService


def get_current_year() -> int:
    """Resolve calendar year once per request (application owns “now”; domain stays pure)."""
    return datetime.now().year


def get_gis_service() -> GisRateAdjustmentPort:
    """GIS adapter implementing ``GisRateAdjustmentPort`` (mock for Phase 3–4)."""
    return MockGisService()


def get_settings() -> Settings:
    """Load tariff coefficients from environment / optional ``.env``."""
    return Settings()


def get_simulate_use_case(
    gis_rate_adjustment: Annotated[GisRateAdjustmentPort, Depends(get_gis_service)],
    settings: Annotated[Settings, Depends(get_settings)],
) -> SimulatePremiumUseCase:
    """Wire ``PremiumCalculator`` + GIS into ``SimulatePremiumUseCase``."""
    calculator = PremiumCalculator(policy=settings.premium_calculation_policy())
    return SimulatePremiumUseCase(calculator=calculator, gis_rate_adjustment=gis_rate_adjustment)
