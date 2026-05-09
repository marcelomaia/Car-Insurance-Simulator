"""Application settings loaded from environment / optional ``.env`` (defaults match readme tariff tables)."""

from decimal import Decimal

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

from domain.services.premium_calculation import PremiumCalculationPolicy


class Settings(BaseSettings):
    """Tariff coefficients for ``PremiumCalculationPolicy``; override via ``CAR_INSURANCE_*`` env vars."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_prefix="CAR_INSURANCE_",
        extra="ignore",
    )

    base_coverage_percentage: Decimal = Field(default=Decimal("1"))
    rate_per_age_year: Decimal = Field(default=Decimal("0.005"))
    rate_per_value_chunk: Decimal = Field(default=Decimal("0.005"))
    value_chunk_size: Decimal = Field(default=Decimal("10000"))

    def premium_calculation_policy(self) -> PremiumCalculationPolicy:
        """Build the domain policy value object from configured coefficients."""
        return PremiumCalculationPolicy(
            base_coverage_percentage=self.base_coverage_percentage,
            rate_per_age_year=self.rate_per_age_year,
            rate_per_value_chunk=self.rate_per_value_chunk,
            value_chunk_size=self.value_chunk_size,
        )
