"""Deterministic mock GIS: SHA-256 of normalized address → additive rate delta in ``[-0.02, 0.02)``.

GIS adjusts the intrinsic decimal rate **additively**; see ``PremiumCalculator.compute_applied_rate``.
"""

import hashlib
from decimal import Decimal

from domain.ports.gis_rate_adjustment import GisRateAdjustmentPort
from domain.value_objects.address import Address


def _additive_variation_from_digest(digest: bytes) -> Decimal:
    numerator = Decimal(int.from_bytes(digest[:8], "big"))
    scale = numerator / Decimal(2**64)
    return Decimal("-0.02") + scale * Decimal("0.04")


def _utf8_payload(address: Address) -> bytes:
    parts = [
        address.city.strip().lower(),
        address.country.strip().lower(),
        (address.postal_code or "").strip().lower(),
        (address.street or "").strip().lower(),
    ]
    return "|".join(parts).encode("utf-8")


class MockGisService(GisRateAdjustmentPort):
    """Stable variation per location string; same address → same delta across processes."""

    def rate_variation_for_address(self, address: Address) -> Decimal:
        digest = hashlib.sha256(_utf8_payload(address)).digest()
        return _additive_variation_from_digest(digest)
