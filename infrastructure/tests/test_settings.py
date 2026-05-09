"""Tests for ``Settings`` defaults and mapping to ``PremiumCalculationPolicy``."""

from decimal import Decimal

from infrastructure.config.settings import Settings


def test_premium_calculation_policy_reflects_defaults():
    settings = Settings()
    policy = settings.premium_calculation_policy()
    assert policy.base_coverage_percentage == Decimal("1")
    assert policy.rate_per_age_year == Decimal("0.005")
    assert policy.rate_per_value_chunk == Decimal("0.005")
    assert policy.value_chunk_size == Decimal("10000")


def test_settings_reads_env_overrides(monkeypatch):
    monkeypatch.setenv("CAR_INSURANCE_RATE_PER_AGE_YEAR", "0.01")
    monkeypatch.setenv("CAR_INSURANCE_VALUE_CHUNK_SIZE", "5000")
    settings = Settings()
    assert settings.rate_per_age_year == Decimal("0.01")
    assert settings.value_chunk_size == Decimal("5000")
    policy = settings.premium_calculation_policy()
    assert policy.rate_per_age_year == Decimal("0.01")
    assert policy.value_chunk_size == Decimal("5000")
