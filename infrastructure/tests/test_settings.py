"""Tests for ``Settings`` defaults, env overrides, and validation failures."""

from decimal import Decimal

import pytest
from pydantic import ValidationError

from infrastructure.config.settings import Settings


def test_premium_calculation_policy_reflects_defaults(clear_car_insurance_env):
    settings = Settings(_env_file=None)
    policy = settings.premium_calculation_policy()
    assert policy.base_coverage_percentage == Decimal("1")
    assert policy.rate_per_age_year == Decimal("0.005")
    assert policy.rate_per_value_chunk == Decimal("0.005")
    assert policy.value_chunk_size == Decimal("10000")


def test_settings_accepts_high_precision_decimal_strings(clear_car_insurance_env, monkeypatch):
    monkeypatch.setenv("CAR_INSURANCE_RATE_PER_AGE_YEAR", "0.0050000001")
    settings = Settings(_env_file=None)
    assert settings.rate_per_age_year == Decimal("0.0050000001")


def test_settings_reads_env_overrides(clear_car_insurance_env, monkeypatch):
    monkeypatch.setenv("CAR_INSURANCE_RATE_PER_AGE_YEAR", "0.01")
    monkeypatch.setenv("CAR_INSURANCE_VALUE_CHUNK_SIZE", "5000")
    settings = Settings(_env_file=None)
    assert settings.rate_per_age_year == Decimal("0.01")
    assert settings.value_chunk_size == Decimal("5000")
    policy = settings.premium_calculation_policy()
    assert policy.rate_per_age_year == Decimal("0.01")
    assert policy.value_chunk_size == Decimal("5000")


def test_settings_rejects_non_numeric_env_for_decimal_field(clear_car_insurance_env, monkeypatch):
    monkeypatch.setenv("CAR_INSURANCE_BASE_COVERAGE_PERCENTAGE", "not-a-decimal")
    with pytest.raises(ValidationError):
        Settings(_env_file=None)
