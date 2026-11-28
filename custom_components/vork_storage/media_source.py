"""The libraries as a media source: folders, photos, videos and music."""

from __future__ import annotations

from urllib.parse import quote

from homeassistant.components.media_player import BrowseError, MediaClass, MediaType
from homeassistant.components.media_source import (
    BrowseMediaSource,
    MediaSource,
    MediaSourceItem,
    PlayMedia,
    Unresolvable,
)
from homeassistant.core import HomeAssistant

from .client import VorkStorage, VorkStorageError
from .const import DOMAIN
from .view import content_type

TITLE = "vØrk storage"


async def async_get_media_source(hass: HomeAssistant) -> MediaSource:
    return VorkMediaSource(hass)


def _split(identifier: str | None) -> tuple[str, str]:
    """`<library>:<path>` (no identifier: the libraries)."""
    if not identifier:
        return "", ""
    ns, _, path = identifier.partition(":")
    return ns, path or "/"


def _media_class(mime: str) -> str | None:
    """A file's media class; None: not media."""
    if mime.startswith("image/"):
        return MediaClass.IMAGE
    if mime.startswith("video/"):
        return MediaClass.VIDEO
    if mime.startswith("audio/"):
        return MediaClass.MUSIC
    return None


def _dir(identifier: str, title: str) -> BrowseMediaSource:
    return BrowseMediaSource(
        domain=DOMAIN,
        identifier=identifier,
        media_class=MediaClass.DIRECTORY,
        media_content_type=MediaType.PLAYLIST,
        title=title,
        can_play=False,
        can_expand=True,
    )


class VorkMediaSource(MediaSource):
    """vØrk storage's libraries, through the add-on."""

    name = TITLE

    def __init__(self, hass: HomeAssistant) -> None:
        super().__init__(DOMAIN)
        self.hass = hass

    def _client(self) -> VorkStorage:
        client = self.hass.data.get(DOMAIN, {}).get("client")
        if client is None:
            raise BrowseError("vØrk storage isn't set up")
        return client

    async def async_resolve_media(self, item: MediaSourceItem) -> PlayMedia:
        ns, path = _split(item.identifier)
        if not ns or path == "/":
            raise Unresolvable("not a file")
        name = path.rsplit("/", 1)[-1]
        return PlayMedia(f"/api/vork_storage/file/{quote(ns, safe='')}{quote(path)}", content_type(name))

    async def async_browse_media(self, item: MediaSourceItem) -> BrowseMediaSource:
        client = self._client()
        ns, path = _split(item.identifier)
        try:
            if not ns:
                libraries = await client.libraries()
                children = [_dir(f"{lib['name']}:/", lib["name"]) for lib in libraries]
                return self._folder(None, TITLE, children)
            entries = await client.list(ns, path)
        except VorkStorageError as e:
            raise BrowseError(str(e)) from e
        children = []
        for e in sorted(entries, key=lambda e: (not e["dir"], e["name"].lower())):
            if e["dir"]:
                children.append(_dir(f"{ns}:{e['path']}", e["name"]))
                continue
            mime = e.get("type", "")
            media_class = _media_class(mime)
            if media_class is None:
                continue
            children.append(
                BrowseMediaSource(
                    domain=DOMAIN,
                    identifier=f"{ns}:{e['path']}",
                    media_class=media_class,
                    media_content_type=mime,
                    title=e["name"],
                    can_play=True,
                    can_expand=False,
                )
            )
        title = ns if path == "/" else path.rsplit("/", 1)[-1]
        return self._folder(f"{ns}:{path}", title, children)

    @staticmethod
    def _folder(identifier: str | None, title: str, children: list[BrowseMediaSource]) -> BrowseMediaSource:
        classes = {c.media_class for c in children}
        return BrowseMediaSource(
            domain=DOMAIN,
            identifier=identifier,
            media_class=MediaClass.DIRECTORY,
            media_content_type=MediaType.PLAYLIST,
            children_media_class=classes.pop() if len(classes) == 1 else MediaClass.DIRECTORY,
            title=title,
            can_play=False,
            can_expand=True,
            children=children,
        )
