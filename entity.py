"""Base class for ColorBeam devices."""

from pycolorbeam import ColorBeamBaseInstance,ColorBeamLightInstance,ColorBeamRGBLightInstance

from homeassistant.const import ATTR_IDENTIFIERS, ATTR_VIA_DEVICE
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.entity import Entity
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_HOST,CONF_PORT

from .const import DOMAIN

class ColorBeamBaseEntity(Entity):
    """Base class for ColorBeam entities."""

    _attr_should_poll = True
    _attr_has_entity_name = True

    def __init__(
            self,ColorBeamDeviceUuid: ConfigEntry.entry_id
    )-> None:
        """initalize the device."""
        self._uuid = ColorBeamDeviceUuid

    async def async_added_to_hass(self) -> None:
        """Register callbacks."""
        

    def _request_state(self) -> None:
        """Request the state."""

    def _update_attrs(self) -> None:
        """Update the entity's attributes."""

    def _update_callback(
            self,_context: None,_params:dict
    )-> None:
        """RUn when invoked by pycolorbeam when the device state changes."""
        self._update_attrs()
        self.schedule_update_ha_state()
    
    @property
    def unique_id(self)->str:
        """Return a unique ID."""

        return self._uuid
    
    def update(self)->None:
        """Update the entity's state."""
        self._request_state()
        self._update_attrs()

class ColorBeamLightDevice(ColorBeamBaseEntity):
    """Representation of a ColorBeam Light Device"""

    def __init__(
            self
    )->None:


        
