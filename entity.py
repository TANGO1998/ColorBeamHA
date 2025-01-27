"""Base class for ColorBeam devices."""
from homeassistant.helpers import device_registry as dr
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN
from .coordinator import ColorBeamUpdateCoordinator

class ColorBeamBaseEntity(CoordinatorEntity):
    """Base class for ColorBeam entities."""

    _attr_should_poll = True
    _attr_has_entity_name = True

    @property
    def deviceInfo(self)->DeviceInfo:
        """Return device Info"""
        version = self.coordinator.version
        return DeviceInfo(
            identifiers={(DOMAIN,"B8:27:EB:5A:56:B0")},
            name="colorbeam light",
            manufacturer="ColorBeam",
            sw_version=version,
        )
    
