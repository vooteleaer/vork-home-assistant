"""vØrk storage in Home Assistant's media browser.

The vØrk storage add-on's page (vork-web) answers read-only `/media/` calls
to whoever holds its media token: the libraries, a folder's files, a file's
content with byte ranges. This integration shows them as a media source and
passes the files on to the browser or a media player through Home
Assistant (`/api/vork_storage/file/...`, signed like any media URL), so the
add-on needn't be reachable from anywhere else. Nothing is copied.
"""

from __future__ import annotations

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .const import DOMAIN
from .client import VorkStorage
from .view import VorkFileView


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up the add-on's client and the file view."""
    data = hass.data.setdefault(DOMAIN, {})
    data["client"] = VorkStorage(hass, entry.data)
    if not data.get("view"):
        hass.http.register_view(VorkFileView(hass))
        data["view"] = True
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Forget the client (the view stays registered and answers 404)."""
    hass.data.get(DOMAIN, {}).pop("client", None)
    return True
