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

    _async_check_entity_unique_id(
        hass,
        entity_registry,
        platform,
        output.uuid,
        output.legacy_uuid,
        entry_data.client.guid,
    )
    _async_check_device_identifiers(
        hass,
        device_registry,
        output.uuid,
        output.legacy_uuid,
        entry_data.client.guid,
    )
    
def _async_check_entity_unique_id(
    hass: HomeAssistant,
    entity_registry: er.EntityRegistry,
    platform: str,
    uuid: str,
    legacy_uuid: str,
    controller_guid: str,
) -> None:
    """If uuid becomes available update to use it."""

    if not uuid:
        return

    unique_id = f"{controller_guid}_{legacy_uuid}"
    entity_id = entity_registry.async_get_entity_id(
        domain=platform, platform=DOMAIN, unique_id=unique_id
    )

    if entity_id:
        new_unique_id = f"{controller_guid}_{uuid}"
        _LOGGER.debug("Updating entity id from %s to %s", unique_id, new_unique_id)
        entity_registry.async_update_entity(entity_id, new_unique_id=new_unique_id)


def _async_check_device_identifiers(
    hass: HomeAssistant,
    device_registry: dr.DeviceRegistry,
    uuid: str,
    legacy_uuid: str,
    controller_guid: str,
) -> None:
    """If uuid becomes available update to use it."""

    if not uuid:
        return

    unique_id = f"{controller_guid}_{legacy_uuid}"
    device = device_registry.async_get_device(identifiers={(DOMAIN, unique_id)})
    if device:
        new_unique_id = f"{controller_guid}_{uuid}"
        _LOGGER.debug("Updating device id from %s to %s", unique_id, new_unique_id)
        device_registry.async_update_device(
            device.id, new_identifiers={(DOMAIN, new_unique_id)}
        )


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Clean up resources and entities associated with the integration."""
    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)