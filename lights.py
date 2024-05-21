from __future__ import annotations

import logging

import awesomelights
import voluptuous as vol
from colorbeam import ColorBeamLightInstance

# Import the device class from the component that you want to support
import homeassistant.helpers.config_validation as cv
from homeassistant.components.light import (SUPPORT_BRIGHTNESS,SUPPORT_COLOR_TEMP,ATTR_COLOR_TEMP_KELVIN,ATTR_BRIGHTNESS, PLATFORM_SCHEMA,
                                            LightEntity)
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
    vol.Required(CONF_TYPE): cv.string
})

def setup_platform(
    hass: HomeAssistant,
    config: ConfigType,
    add_entities: AddEntitiesCallback,
    discovery_info: DiscoveryInfoType | None = None
) -> None:
    """Set up the ColorBeam Light platform."""
    # Assign configuration variables.
    # The configuration check takes care they are present.
    # id = config[CONF_HOST]
    # username = config[CONF_USERNAME]
    # password = config.get(CONF_PASSWORD)

    # # Setup connection with devices/cloud
    # hub = awesomelights.Hub(host, username, password)

    # # Verify that passed in configuration works
    # if not hub.is_valid_login():
    #     _LOGGER.error("Could not connect to AwesomeLight hub")
    #     return

    light = {
        "IP" : config[CONF_IP_ADDRESS],
        "PORT" : config[CONF_PORT],
        "NAME" : config[CONF_NAME],
        "ID" : config[CONF_ID]
    }
    # Add devices
    add_entities([CbLight(light)])


class CbLight(LightEntity):
    """Representation of an ColorBeam Light."""

    def __init__(self, light) -> None:
        """Initialize an AwesomeLight."""
        self._light = ColorBeamLightInstance(light["IP"],light["PORT"],light["ID"])
        self._name = light["NAME"]
        self._state = self._light.is_on()
        self._brightness = self._light.Getbrightness()

    @property
    def name(self) -> str:
        """Return the display name of this light."""
        return self._name

    @property
    def brightness(self):
        """Return the brightness of the light.

        This method is optional. Removing it indicates to Home Assistant
        that brightness is not supported for this light.
        """
        return self._brightness

    @property
    def is_on(self) -> bool | None:
        """Return true if light is on."""
        return self._state

    def turn_on(self, **kwargs: Any) -> None:
        """Instruct the light to turn on.

        You can skip the brightness part if your light does not support
        brightness control.
        """
        if kwargs.get(ATTR_BRIGHTNESS):
            self._light.setBrightness(kwargs.get(ATTR_BRIGHTNESS,255))
        elif kwargs.get(ATTR_COLOR_TEMP_KELVIN):
            self._light.setTemp(kwargs.get(ATTR_COLOR_TEMP_KELVIN))
            self._light.turn_on()
        else:
            self._light.turn_on()

    def turn_off(self, **kwargs: Any) -> None:
        """Instruct the light to turn off."""
        self._light.turn_off()

    def update(self) -> None:
        """Fetch new state data for this light.

        This is the only method that should fetch new data for Home Assistant.
        """
        self._light.update()
        self._state = self._light.is_on()
        self._brightness = self._light.Getbrightness()