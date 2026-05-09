from abc import ABC, abstractmethod

from domain.value_objects.address import Address


class GisRateAdjustmentPort(ABC):
    @abstractmethod
    def rate_variation_for_address(self, address: Address) -> float:
        """Return additive rate delta in [-0.02, 0.02] for GIS risk adjustment."""
