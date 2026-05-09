"""HTTP-level tests for premium simulation (FastAPI ``TestClient``)."""

from decimal import Decimal

import pytest
from fastapi.testclient import TestClient

from domain.exceptions import DomainError
from domain.ports.gis_rate_adjustment import GisRateAdjustmentPort
from domain.value_objects.address import Address
from infrastructure.config.settings import Settings
from presentation.app import create_app
from presentation.deps import get_current_year, get_gis_service, get_settings, get_simulate_use_case


class _MinusFiveGis(GisRateAdjustmentPort):
    def rate_variation_for_address(self, address: Address) -> Decimal:
        return Decimal("-0.05")


class _RaisesDomainError:
    def execute(self, inputs):
        raise DomainError("generic failure")


def test_health_endpoint_returns_ok():
    client = TestClient(create_app())
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_simulate_generic_domain_error_returns_domain_error_code():
    application = create_app()
    application.dependency_overrides[get_current_year] = lambda: 2026
    application.dependency_overrides[get_simulate_use_case] = lambda: _RaisesDomainError()
    client = TestClient(application)
    response = client.post(
        "/v1/premium/simulate",
        json={
            "broker_fee": 0,
            "deductible_percentage": 0.1,
            "make": "A",
            "model": "B",
            "value": 10000,
            "year": 2020,
        },
    )
    assert response.status_code == 422
    assert response.json()["detail"]["code"] == "domain_error"


def test_simulate_invalid_deductible_returns_422_domain_code():
    application = create_app()
    application.dependency_overrides[get_current_year] = lambda: 2026
    client = TestClient(application)
    response = client.post(
        "/v1/premium/simulate",
        json={
            "broker_fee": 0,
            "deductible_percentage": 3,
            "make": "A",
            "model": "B",
            "value": 5000,
            "year": 2024,
        },
    )
    assert response.status_code == 422
    assert response.json()["detail"]["code"] == "invalid_deductible_percentage"


def test_simulate_negative_applied_rate_returns_422():
    application = create_app()
    application.dependency_overrides[get_current_year] = lambda: 2026
    application.dependency_overrides[get_gis_service] = lambda: _MinusFiveGis()
    client = TestClient(application)
    response = client.post(
        "/v1/premium/simulate",
        json={
            "broker_fee": 0,
            "deductible_percentage": 0,
            "make": "Mini",
            "model": "Risk",
            "registration_location": {"city": "X", "country": "Y"},
            "value": 0,
            "year": 2026,
        },
    )
    assert response.status_code == 422
    assert response.json()["detail"]["code"] == "negative_applied_rate"


def test_simulate_success_matches_readme_decade_example(clear_car_insurance_env):
    application = create_app()
    application.dependency_overrides[get_current_year] = lambda: 2026
    application.dependency_overrides[get_settings] = lambda: Settings(_env_file=None)
    client = TestClient(application)
    response = client.post(
        "/v1/premium/simulate",
        json={
            "broker_fee": 50,
            "deductible_percentage": 0.1,
            "make": "Toyota",
            "model": "Corolla",
            "value": 100000,
            "year": 2016,
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["applied_rate"] == pytest.approx(0.10)
    assert data["calculated_premium"] == pytest.approx(9050)
    assert data["deductible_value"] == pytest.approx(10000)
    assert data["policy_limit"] == pytest.approx(90000)
