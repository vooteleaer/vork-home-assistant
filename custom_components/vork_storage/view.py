"""The files, passed on from the add-on to the browser or a media player."""

from __future__ import annotations

from http import HTTPStatus

import aiohttp
from aiohttp import web

from homeassistant.components.http import HomeAssistantView
from homeassistant.core import HomeAssistant

from .const import DOMAIN

PASSED_ON = ("Content-Type", "Content-Length", "Content-Range", "Accept-Ranges", "Cache-Control")


class VorkFileView(HomeAssistantView):
    """`/api/vork_storage/file/<library>/<path>`: signed in, or a signed URL."""

    url = "/api/vork_storage/file/{ns}/{path:.*}"
    name = "api:vork_storage:file"
    requires_auth = True

    def __init__(self, hass: HomeAssistant) -> None:
        self.hass = hass

    async def _answer(self, request: web.Request, ns: str, path: str, head: bool) -> web.StreamResponse:
        client = self.hass.data.get(DOMAIN, {}).get("client")
        if client is None:
            return web.Response(status=HTTPStatus.NOT_FOUND)
        extra = {"Range": request.headers["Range"]} if "Range" in request.headers else None
        method = "HEAD" if head else "GET"
        try:
            upstream = await client.session.request(
                method,
                client.file_url(ns, "/" + path),
                headers=client.headers(extra),
                timeout=aiohttp.ClientTimeout(total=None, sock_connect=10, sock_read=120),
            )
        except aiohttp.ClientError:
            return web.Response(status=HTTPStatus.BAD_GATEWAY)
        try:
            response = web.StreamResponse(status=upstream.status)
            for h in PASSED_ON:
                if h in upstream.headers:
                    response.headers[h] = upstream.headers[h]
            await response.prepare(request)
            if not head:
                async for chunk in upstream.content.iter_chunked(64 << 10):
                    await response.write(chunk)
            await response.write_eof()
            return response
        finally:
            upstream.release()

    async def get(self, request: web.Request, ns: str, path: str) -> web.StreamResponse:
        return await self._answer(request, ns, path, False)

    async def head(self, request: web.Request, ns: str, path: str) -> web.StreamResponse:
        return await self._answer(request, ns, path, True)


TYPES = {
    "jpg": "image/jpeg", "jpeg": "image/jpeg", "png": "image/png", "gif": "image/gif", "webp": "image/webp",
    "heic": "image/heic", "heif": "image/heic", "avif": "image/avif", "bmp": "image/bmp",
    "mp4": "video/mp4", "m4v": "video/mp4", "mov": "video/quicktime", "webm": "video/webm",
    "mkv": "video/x-matroska", "avi": "video/x-msvideo",
    "mp3": "audio/mpeg", "m4a": "audio/mp4", "aac": "audio/mp4", "flac": "audio/flac",
    "ogg": "audio/ogg", "oga": "audio/ogg", "opus": "audio/opus", "wav": "audio/wav",
}


def content_type(name: str) -> str:
    """A file's type by its name (as vork-web says it)."""
    ext = name.rsplit(".", 1)[-1].lower() if "." in name else ""
    return TYPES.get(ext, "application/octet-stream")
