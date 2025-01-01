"""Coordinator for the ColorBeam integration."""

import asyncio
from datetime import timedelta
import logging
from typing import cast

import pycolorbeam

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

UPDATE_INTERVAL = 10

class ColorBeamUpdateCoordinator(DataUpdateCoordinator[dict]):
    """Update coordinator for ColorBeam data."""
    def __init__(self,hass: HomeAssistant,client:)
    super().__init__(
        hass,
        logger=LOGGER,
        name=DOMAIN,
        update_interal=timedelta(UPDATE_INTERVAL),
    )
    self.client = client

    async def _async_update_data(self) -> dict:
        """Update Evil Genius data."""
        