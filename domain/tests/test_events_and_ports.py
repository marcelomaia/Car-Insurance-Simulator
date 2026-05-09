"""Coverage for domain events package, ports package, and GIS port contract."""

from decimal import Decimal

import domain.events
import domain.ports
from domain.entities.car import Car
from domain.events.premium_calculated import PremiumCalculated
from domain.ports.gis_rate_adjustment import GisRateAdjustmentPort
from domain.value_objects.address import Address


class FakeGisRateAdjustment(GisRateAdjustmentPort):
    def rate_variation_for_address(self, address: Address) -> Decimal:
        return Decimal("0")


def test_domain_ports_exports_gis_rate_adjustment_port():
    assert "GisRateAdjustmentPort" in domain.ports.__all__
    assert domain.ports.GisRateAdjustmentPort is GisRateAdjustmentPort


def test_events_package_exports_premium_calculated():
    assert "PremiumCalculated" in domain.events.__all__
    assert domain.events.PremiumCalculated is PremiumCalculated


def test_gis_rate_adjustment_port_implementation_returns_decimal():
    gis = FakeGisRateAdjustment()
    address = Address(city="Lisbon", country="PT")
    assert gis.rate_variation_for_address(address) == Decimal("0")


def test_premium_calculated_event_is_constructible():
    car = Car(make="Acme", model="Roadster", value=Decimal("50000"), year=2022)
    event = PremiumCalculated(
        applied_rate=Decimal("0.12"),
        calculated_premium=Decimal("6000"),
        car=car,
        deductible_value=Decimal("500"),
        policy_limit=Decimal("45000"),
    )
    assert event.car is car
    assert event.applied_rate == Decimal("0.12")
