"""Shared pytest helpers (isolate tests from developer ``.env`` / shell exports)."""

import pytest

CAR_INSURANCE_ENV_KEYS = (
    "CAR_INSURANCE_BASE_COVERAGE_PERCENTAGE",
    "CAR_INSURANCE_RATE_PER_AGE_YEAR",
    "CAR_INSURANCE_RATE_PER_VALUE_CHUNK",
    "CAR_INSURANCE_VALUE_CHUNK_SIZE",
)


@pytest.fixture
def clear_car_insurance_env(monkeypatch: pytest.MonkeyPatch) -> None:
    """Drop ``CAR_INSURANCE_*`` from the process env so ``Settings`` reflects only explicit monkeypatch / defaults."""
    for key in CAR_INSURANCE_ENV_KEYS:
        monkeypatch.delenv(key, raising=False)
