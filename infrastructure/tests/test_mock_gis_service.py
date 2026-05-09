"""Tests for ``MockGisService``: deterministic hashing and additive delta bounds."""

from decimal import Decimal

from domain.value_objects.address import Address
from infrastructure.gis.mock_gis_service import MockGisService


def test_rate_variation_deterministic_for_identical_address():
    service = MockGisService()
    address = Address(city="Lisbon", country="PT", postal_code="1000-001", street="Rua A")
    first = service.rate_variation_for_address(address)
    second = service.rate_variation_for_address(address)
    assert first == second


def test_rate_variation_ignores_case_and_outer_whitespace():
    service = MockGisService()
    a = Address(city="  Lisbon  ", country="pt")
    b = Address(city="lisbon", country="PT")
    assert service.rate_variation_for_address(a) == service.rate_variation_for_address(b)


def test_rate_variation_strictly_below_upper_bound():
    service = MockGisService()
    address = Address(city="Tokyo", country="JP")
    variation = service.rate_variation_for_address(address)
    assert variation < Decimal("0.02")


def test_rate_variation_within_documented_closed_interval():
    service = MockGisService()
    for city in ("A", "B", "ZZ", "North", "South"):
        address = Address(city=city, country="XY")
        variation = service.rate_variation_for_address(address)
        assert Decimal("-0.02") <= variation <= Decimal("0.02")
