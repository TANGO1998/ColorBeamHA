"""represenation of a ColorBeam BI Light"""

from dataclasses import dataclass
import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_HOST,CONF_PORT, Platform
from homeassistant.core import HomeAssistant
from homeassistant.helpers import device_registry as dr, entity_registry as er

from .const import DOMAIN
from .pycolorbeam import ColorBeamBaseInstance,ColorBeamLightInstance,ColorBeamRGBLightInstance
PLATFORMS = [
    Platform.LIGHT,
]

_LOGGER = logging.getLogger(__name__)
ATTR_ACTION = "action"
ATTR_FULL_ID = "full_id"
ATTR_UUID = "uuid"

@dataclass(slots=True, kw_only=True)
class ColorBeamData:
    """Storage class for platform global data."""
    lights: list[tuple[str, Output]]

async def async_setup_entry(hass: HomeAssistant, config_entry: ConfigEntry) -> bool:
    """Set up the ColorBeam integration."""

    host = config_entry.data[CONF_HOST]
    port = config_entry.data[CONF_PORT]


    colorbeam_client = ColorBeamBaseInstance(host,port)
    _LOGGER.info("connecting to gateway")
    RGB , BI = await hass.async_add_executor_job(colorbeam_client.updateall())
    
    entity_registry = er.async_get(hass)
    device_registry = dr.async_get(hass)

    _LOGGER.info("adding devices")
    
    entry_data = ColorBeamData(
        lights = []
    )

    