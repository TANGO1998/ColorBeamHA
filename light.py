from __future__ import annotations

import logging
import asyncio

import voluptuous as vol
import uuid
from typing import Any
from .pycolorbeam import ColorBeamBaseInstance,ColorBeamLightInstance,ColorBeamRGBLightInstance

# Import the device class from the component that you want to support
import homeassistant.helpers.config_validation as cv
from homeassistant.components.light import (ColorMode,ATTR_COLOR_TEMP_KELVIN,ATTR_BRIGHTNESS,ATTR_TRANSITION, ATTR_RGB_COLOR,
                                            LightEntity,LightEntityFeature)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant,callback
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from .coordinator import ColorBeamUpdateCoordinator,ColorBeamBiUpdateCoordinator,ColorBeamRGBUpdateCoordinator
from .const import DOMAIN
from .entity import ColorBeamBaseEntity

_LOGGER = logging.getLogger("colorbeam")


async def async_setup_platform(
    hass: HomeAssistant,
    entry: ConfigEntry,
    add_entities: AddEntitiesCallback,
) -> None:
    """Set up the ColorBeam Light platform."""
    coordinator : ColorBeamUpdateCoordinator = hass.data[DOMAIN][entry.entry_id]

    for RGB in coordinator.RGBlights:
        light = {
            "ip" : entry.data["host"],
            "port" :entry.data["port"],
            "name" : "colorBeamRGB" + RGB,
            "id" : RGB,
            "uuid" : uuid.uuid4()
        }
        # Add devices
        add_entities([CbRGBLight(light)],True)

    for BI in coordinator.BIlights:
        light = {
            "ip" : entry.data["host"],
            "port" :entry.data["port"],
            "name" : "colorBeamBI" + BI,
            "id" : BI,
            "uuid" : uuid.uuid4()
        }
        # Add devices
        add_entities([CbBiLight(light)],True)



class CbBiLight(LightEntity,ColorBeamBaseEntity):
    """Representation of an ColorBeam Light."""
    _attr_color_mode = ColorMode.COLOR_TEMP
    _attr_supported_color_modes = {ColorMode.COLOR_TEMP}
    _attr_supported_features = LightEntityFeature.TRANSITION
    _attr_min_temp_kelvin = 2000
    _attr_max_temp_kelvin = 7000

    def __init__(self, light) -> None:
        """Initialize a ColorBeamLight."""
        self._light = ColorBeamLightInstance(light["ip"],light["port"],light["id"])
        self._name = light["name"]
        self._state = None
        self._attr_brightness = None
        self._previous_brightness = 255
        self._attr_color_temp_kelvin = None
        self._attr_unique_id = light["uuid"]

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
        if ATTR_BRIGHTNESS in kwargs:
            brightness = kwargs.get(ATTR_BRIGHTNESS)
        elif self._previous_brightness == 0:
            brightness = 255/2
        else:
            brightness = self._previous_brightness
        if ATTR_COLOR_TEMP_KELVIN in kwargs:
            tempurature = kwargs.get(ATTR_COLOR_TEMP_KELVIN)
        else:
            tempurature = 3200
        if ATTR_TRANSITION in kwargs:
            await self._light.setTemp(tempurature)
            await self._light.turn_on(brightness,ATTR_TRANSITION)
        else:
            await self._light.setTemp(tempurature)
            await self._light.turn_on(brightness)
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

class CbRGBLight(LightEntity,ColorBeamBaseEntity):
    """Representation of an ColorBeam Light."""
    _attr_color_mode = ColorMode.RGB
    _attr_supported_color_modes = {ColorMode.RGB}
    _attr_supported_features = LightEntityFeature.TRANSITION

    def __init__(self, light) -> None:
        """Initialize a ColorBeamLight."""
        self._light = ColorBeamRGBLightInstance(light["ip"],light["port"],light["id"])
        self._name = light["name"]
        self._state = None
        self._attr_brightness = None
        self._previous_brightness = 255
        self. _attr_rgb_color = (0,0,0)
        self._attr_unique_id = light["uuid"]

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
    def rgb_color(self) -> tuple | None:
        """Return Color Temp"""
        return self._attr_rgb_color
    @property
    def should_poll(self):
        return True

    async def async_turn_on(self, **kwargs: Any) -> None:
        """Instruct the light to turn on.

        You can skip the brightness part if your light does not support
        brightness control.
        """
        if ATTR_BRIGHTNESS in kwargs:
            brightness = kwargs.get(ATTR_BRIGHTNESS)
        elif self._previous_brightness == 0:
            brightness = 255/2
        else:
            brightness = self._previous_brightness
        if ATTR_RGB_COLOR in kwargs:
            rgb_color = kwargs.pop(ATTR_RGB_COLOR)
        else:
            rgb_color = (255,255,255)
        if ATTR_TRANSITION in kwargs:
            await self._light.setRGB(rgb_color)
            await self._light.turn_on(brightness,kwargs.get(ATTR_TRANSITION))
        else:
            await self._light.setRGB(rgb_color)
            await self._light.turn_on(brightness)
        await self._light.update()

    async def async_turn_off(self, **kwargs: Any) -> None:
        """Instruct the light to turn off."""
        await self._light.turn_off()

    async def async_update(self) -> None:
        """Fetch new state data for this light.

        This is the only method that should fetch new data for Home Assistant.
        """
        await self._light.update()
        self. _attr_rgb_color = self._light.getRGB
        self._state = self._light.is_on
        self._attr_brightness = self._light.Getbrightness