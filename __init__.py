"""represenation of a ColorBeam BI Light"""

from dataclasses import dataclass
import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_HOST, CONF_PASSWORD, CONF_USERNAME, Platform
from homeassistant.core import HomeAssistant
from homeassistant.helpers import device_registry as dr, entity_registry as er

from .const import DOMAIN

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

