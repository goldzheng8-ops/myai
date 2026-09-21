import asyncio
import sys
import types
import pytest
import httpx

# Provide minimal jsonpath_ng stub to avoid heavy dependency during tests
jsonpath_ng = types.ModuleType("jsonpath_ng")
jsonpath_ng_ext = types.ModuleType("jsonpath_ng.ext")
def _parse(expr):
    def _noop(data):
        return []
    return _noop
jsonpath_ng_ext.parse = _parse
sys.modules["jsonpath_ng"] = jsonpath_ng
sys.modules["jsonpath_ng.ext"] = jsonpath_ng_ext

from core.request.context import RequestContext
from core.request.descriptor import RequestDescriptor
from core.request.profile import RequestProfile
from core.request.typing import HttpMethod
from core.request.typing import ResponseFormat, RequestKind
from core.request.downloader.httpx import HttpxDownloader
from core.request.downloader.config import HttpxDownloaderConfig
from core.request.downloader.result import DownloadResult


class DummyResponseAdapterResolver:
    def resolve(self, *, profile, response):
        return object()


def test_stream(monkeypatch):
    async def _run():
        # Build minimal context
        descriptor = RequestDescriptor(
            url="https://httpbin.org/stream/3",
            kind=RequestKind.LIST,
            profile=RequestProfile(downloader=None, response_format=ResponseFormat.BINARY),
            target_spider="test",
            method=HttpMethod.GET,
        )

        context = RequestContext(descriptor=descriptor, configs=())

        resolver = DummyResponseAdapterResolver()
        downloader = HttpxDownloader(resolver, HttpxDownloaderConfig())

        result = await downloader.stream(context)

        assert isinstance(result, DownloadResult)
        assert result.is_streaming

        # consume stream
        collected = b""
        async for chunk in result.stream:
            collected += chunk

        assert collected

    asyncio.run(_run())
