"""Behaviour of immutable domain dataclasses (equality, hashing, optional fields)."""

from dataclasses import FrozenInstanceError
from decimal import Decimal

import pytest

from domain.entities.car import Car
from domain.events.premium_calculated import PremiumCalculated
from domain.value_objects.address import Address


def test_address_equality_uses_all_fields_including_optionals():
    a = Address(city="Lisbon", country="PT", postal_code="1200", street="Rua 1")
    b = Address(city="Lisbon", country="PT", postal_code="1200", street="Rua 1")
    c = Address(city="Lisbon", country="PT", postal_code=None, street=None)
    assert a == b
    assert a != c


def test_address_optional_none_vs_omitted_equivalent():
    explicit = Address(city="X", country="Y", postal_code=None, street=None)
    omitted = Address(city="X", country="Y")
    assert explicit == omitted


def test_car_dataclass_equality_and_hashable_when_frozen():
    car_a = Car(make="Toyota", model="Corolla", value=Decimal("1"), year=2020)
    car_b = Car(make="Toyota", model="Corolla", value=Decimal("1"), year=2020)
    car_c = Car(make="Toyota", model="Camry", value=Decimal("1"), year=2020)
    assert car_a == car_b
    assert car_a != car_c
    assert hash(car_a) == hash(car_b)


def test_car_value_decimal_precision_matters_for_equality():
    one = Car(make="A", model="B", value=Decimal("1.0"), year=2021)
    also_one = Car(make="A", model="B", value=Decimal("1.00"), year=2021)
    assert one == also_one


def test_premium_calculated_frozen_rejects_mutation():
    car = Car(make="A", model="B", value=Decimal("100"), year=2020)
    event = PremiumCalculated(
        applied_rate=Decimal("0.1"),
        calculated_premium=Decimal("10"),
        car=car,
        deductible_value=Decimal("5"),
        policy_limit=Decimal("95"),
    )
    with pytest.raises(FrozenInstanceError):
        event.calculated_premium = Decimal("99")  # type: ignore[misc]


def test_premium_calculated_identity_car_reference():
    car = Car(make="Hold", model="Ref", value=Decimal("1"), year=2019)
    event = PremiumCalculated(
        applied_rate=Decimal("0"),
        calculated_premium=Decimal("0"),
        car=car,
        deductible_value=Decimal("0"),
        policy_limit=Decimal("0"),
    )
    assert event.car is car
