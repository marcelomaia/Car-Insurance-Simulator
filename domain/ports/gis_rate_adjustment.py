from abc import ABC, abstractmethod
from decimal import Decimal

from domain.value_objects.address import Address


class GisRateAdjustmentPort(ABC):
    @abstractmethod
    def rate_variation_for_address(self, address: Address) -> Decimal:
        """Return additive rate delta in [-0.02, 0.02] for GIS risk adjustment."""
