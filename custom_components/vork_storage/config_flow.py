"""Set up from the add-on's discovery, or by hand (its URL and media token)."""

from __future__ import annotations

from typing import Any

import voluptuous as vol

from homeassistant.config_entries import ConfigFlow, ConfigFlowResult

try:
    from homeassistant.helpers.service_info.hassio import HassioServiceInfo
except ImportError:  # older Home Assistant
    from homeassistant.components.hassio import HassioServiceInfo  # type: ignore[no-redef]

from .client import VorkStorage, VorkStorageError
from .const import CONF_TOKEN, CONF_URL, DOMAIN


class VorkStorageFlow(ConfigFlow, domain=DOMAIN):
    """One vØrk storage add-on."""

    VERSION = 1

    def __init__(self) -> None:
        self._found: dict[str, Any] | None = None

    async def _check(self, conf: dict[str, Any]) -> str | None:
        try:
            await VorkStorage(self.hass, conf).libraries()
        except VorkStorageError:
            return "cannot_connect"
        return None

    async def async_step_hassio(self, discovery_info: HassioServiceInfo) -> ConfigFlowResult:
        """The add-on said where it is (again after each start: a new address is taken)."""
        await self.async_set_unique_id(DOMAIN)
        c = discovery_info.config
        conf = {CONF_URL: f"http://{c['host']}:{c['port']}", CONF_TOKEN: c["token"]}
        self._abort_if_unique_id_configured(updates=conf)
        self._found = conf
        return await self.async_step_hassio_confirm()

    async def async_step_hassio_confirm(self, user_input: dict[str, Any] | None = None) -> ConfigFlowResult:
        assert self._found is not None
        if user_input is not None:
            if error := await self._check(self._found):
                return self.async_abort(reason=error)
            return self.async_create_entry(title="vØrk storage", data=self._found)
        return self.async_show_form(step_id="hassio_confirm")

    async def async_step_user(self, user_input: dict[str, Any] | None = None) -> ConfigFlowResult:
        """By hand: the add-on's URL and the media token from its log."""
        errors: dict[str, str] = {}
        if user_input is not None:
            await self.async_set_unique_id(DOMAIN)
            self._abort_if_unique_id_configured()
            if error := await self._check(user_input):
                errors["base"] = error
            else:
                return self.async_create_entry(title="vØrk storage", data=user_input)
        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(CONF_URL, default=(user_input or {}).get(CONF_URL, "http://")): str,
                    vol.Required(CONF_TOKEN): str,
                }
            ),
            errors=errors,
        )
