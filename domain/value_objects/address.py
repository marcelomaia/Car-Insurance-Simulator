from dataclasses import dataclass


@dataclass(frozen=True)
class Address:
    city: str
    country: str
    postal_code: str | None = None
    street: str | None = None
