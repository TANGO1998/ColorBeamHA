"""Config flow to configure the ColorBeam integration."""

from __future__ import annotations

import logging
from typing import Any
from urllib.error import HTTPError
import uuid

from pycolorbeam import ColorBeamRGBLightInstance,ColorBeamBaseInstance,ColorBeamLightInstance
import voluptuous as vol

from homeassistant.config_entries import ConfigFlow, ConfigFlowResult
from homeassistant.const import CONF_HOST, CONF_PORT

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

class ColorBeamConfigFlow(ConfigFlow, domain=DOMAIN):
    """User prompt for Main Contoller configuration information"""
    VERSION = 1

    async def async_step_user(
            self,user_input: dict[str,Any] | None = None
    ) -> ConfigFlowResult:
        """First step in the config flow."""

        #Check if a configuration entry already exists
        if self._async_current_entries():
            return self.async_abort(Reason="single_instance_allowed")
        
        errors = {}

        if user_input is not None:
            ip_address = user_input[CONF_HOST]
            port = user_input[CONF_PORT]

            main_controller = ColorBeamBaseInstance(CONF_HOST,CONF_PORT)

            try:
                BI , RGB = await self.hass.async_add_executor_job(main_controller.updateall())
            except Exception as e:
                _LOGGER.exception(e)
                errors["base"] = "unknown"

        if not errors:
            await self.async_set_unique_id(f"CB_{uuid.uuid4()}")
            self.abort_if_unique_id_configured()

            return self.async_create_entry(title="ColorBeam",data=user_input)
        
        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(CONF_HOST): str,
                    vol.Required(CONF_PORT,default="3334"):str,
                }
            ),
            errors=errors,
        )
    
