"""Config flow to configure the ColorBeam integration."""

from __future__ import annotations

import logging
from typing import Any
from urllib.error import HTTPError

import voluptuous as vol

from homeassistant.config_entries import ConfigFlow, ConfigFlowResult

from .const import DOMAIN
from .pycolorbeam import ColorBeamBaseInstance

_LOGGER = logging.getLogger(__name__)

class ColorBeamConfigFlow(ConfigFlow, domain=DOMAIN):
    """User prompt for Main Contoller configuration information"""
    VERSION = 1

    async def async_step_user(
            self,user_input: dict[str,Any] | None = None
    ) -> ConfigFlowResult:
        """First step in the config flow."""

        #Check if a configuration entry already exists
        #if self._async_current_entries():
            #return self.async_abort(reason="single_instance_allowed")
        
        errors = {}

        if user_input is None:
            return self.async_show_form(
                step_id="user",
                data_schema=vol.Schema(
                    {
                        vol.Required("host"):str,
                        vol.Required("port",default="3334"):str,
                    }
                ),
            )

        try:
            main_controller = ColorBeamBaseInstance(ipAddress=user_input["host"],port=user_input["port"])
            data = await main_controller.getversion()
        except Exception as e:
            _LOGGER.error(e)
            errors["base"] = e

        else:
            await self.async_set_unique_id(f"CB_GATEWAY_V2_0001")
            self._abort_if_unique_id_configured()

            return self.async_create_entry(title="ColorBeam",
                                           data={
                                               "host": user_input["host"],
                                               "port": user_input["port"]
                                           },)
        
        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required("host"): str,
                    vol.Required("port",default="3334"):str,
                }
            ),
            errors=errors,
        )
    
