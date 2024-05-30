from __future__ import annotations

import logging
import asyncio

import voluptuous as vol
from .colorbeam import ColorBeamLightInstance

# Import the device class from the component that you want to support
import homeassistant.helpers.config_validation as cv
from homeassistant.components.light import (ColorMode,ATTR_COLOR_TEMP_KELVIN,ATTR_BRIGHTNESS,ATTR_TRANSITION, PLATFORM_SCHEMA,
                                            LightEntity,filter_supported_color_modes,LightEntityFeature)
from homeassistant.const import CONF_IP_ADDRESS, CONF_NAME, CONF_PORT, CONF_TYPE, CONF_ID
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType

_LOGGER = logging.getLogger("colorbeam")


# Validation of the user's configuration
PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required(CONF_IP_ADDRESS): cv.string,
    vol.Required(CONF_PORT): cv.string,
    vol.Optional(CONF_NAME): cv.string,
    vol.Required(CONF_ID): cv.string,
})

async def async_setup_platform(
    hass: HomeAssistant,
    config: ConfigType,
    add_entities: AddEntitiesCallback,
    discovery_info: DiscoveryInfoType | None = None
) -> None:
    """Set up the ColorBeam Light platform."""

    light = {
        "ip" : config[CONF_IP_ADDRESS],
        "port" : config[CONF_PORT],
        "name" : config[CONF_NAME],
        "id" : config[CONF_ID]
    }
    # Add devices
    add_entities([CbLight(light)])


class CbLight(LightEntity):
    """Representation of an ColorBeam Light."""
    _attr_color_mode = ColorMode.COLOR_TEMP
    _attr_supported_color_modes = filter_supported_color_modes({ColorMode.COLOR_TEMP})

    def __init__(self, light) -> None:
        """Initialize a ColorBeamLight."""
        self._light = ColorBeamLightInstance(light["ip"],light["port"],light["id"])
        self._name = light["name"]
        self._state = None
        self._attr_brightness = None
        self._previous_brightness = 255
        self._attr_color_temp_kelvin = None
        self._attr_supported_features = LightEntityFeature.TRANSITION

    @property
    def name(self) -> str:
        """Return the display name of this light."""
        return self._name

    @property
    def brightness(self) -> int:
        """Return the brightness of the light.

        This method is optional. Removing it indicates to Home Assistant
        that brightness is not supported for this light.
        """
        return self._attr_brightness

    @property
    def is_on(self) -> bool | None:
        """Return true if light is on."""
        return self._state
    @property
    def color_temp_kelvin(self) -> int | None:
        """Return Color Temp"""
        return self._attr_color_temp_kelvin

    async def async_turn_on(self, **kwargs: Any) -> None:
        """Instruct the light to turn on.

        You can skip the brightness part if your light does not support
        brightness control.
        """
        if kwargs.get(ATTR_BRIGHTNESS):
            await self._light.turn_on(kwargs.get(ATTR_BRIGHTNESS,self._previous_brightness))
        elif kwargs.get(ATTR_COLOR_TEMP_KELVIN):
            await self._light.setTemp(kwargs.get(ATTR_COLOR_TEMP_KELVIN))
            await self._light.turn_on(self._previous_brightness)
        else:
            await self._light.turn_on(self._previous_brightness)

        await self.async_update()

    async def async_turn_off(self, **kwargs: Any) -> None:
        """Instruct the light to turn off."""
        await self._light.turn_off()
        await self.async_update()

    async def async_update(self) -> None:
        """Fetch new state data for this light.

        This is the only method that should fetch new data for Home Assistant.
        """
        self._light.update()
        self._attr_color_temp_kelvin = self._light.Temp
        self._state = self._light.is_on
        self._attr_brightness = self._light.Getbrightness
        self._previous_brightness = self._attr_brightness