"""The vØrk storage add-on's `/media/` calls."""

from __future__ import annotations

from typing import Any
from urllib.parse import urlencode

import aiohttp

from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .const import CONF_TOKEN, CONF_URL


class VorkStorageError(Exception):
    """The add-on didn't answer, or answered an error."""


class VorkStorage:
    """A client of one vork-web's media calls."""

    def __init__(self, hass: HomeAssistant, conf: dict[str, Any]) -> None:
        self.session = async_get_clientsession(hass)
        self.url = conf[CONF_URL].rstrip("/")
        self.token = conf[CONF_TOKEN]

    def headers(self, extra: dict[str, str] | None = None) -> dict[str, str]:
        h = {"Authorization": f"Bearer {self.token}"}
        if extra:
            h.update(extra)
        return h

    async def _json(self, path: str, **query: str) -> Any:
        url = f"{self.url}{path}" + (f"?{urlencode(query)}" if query else "")
        try:
            async with self.session.get(url, headers=self.headers(), timeout=aiohttp.ClientTimeout(total=90)) as r:
                body = await r.json(content_type=None)
                if r.status != 200:
                    raise VorkStorageError(body.get("error") if isinstance(body, dict) else f"HTTP {r.status}")
                return body
        except (aiohttp.ClientError, TimeoutError) as e:
            raise VorkStorageError(str(e)) from e

    async def libraries(self) -> list[dict[str, Any]]:
        """The libraries on the add-on's node (`name`, `for`, `public`)."""
        return await self._json("/media/libraries")

    async def list(self, ns: str, folder: str) -> list[dict[str, Any]]:
        """What's in a folder: `name`, `path`, `dir`, `size`, `type`."""
        return await self._json("/media/list", ns=ns, dir=folder)

    def file_url(self, ns: str, path: str) -> str:
        return f"{self.url}/media/file?{urlencode({'ns': ns, 'path': path})}"
