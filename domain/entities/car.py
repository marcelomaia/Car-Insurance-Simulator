from dataclasses import dataclass
from decimal import Decimal


@dataclass(frozen=True)
class Car:
    make: str
    model: str
    value: Decimal
    year: int
