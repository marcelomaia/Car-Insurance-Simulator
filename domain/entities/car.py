from dataclasses import dataclass


@dataclass(frozen=True)
class Car:
    make: str
    model: str
    value: float
    year: int
