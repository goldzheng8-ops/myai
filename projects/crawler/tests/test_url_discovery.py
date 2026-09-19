from __future__ import annotations

from core.request.discovery.config import HtmlDiscoveryConfig
from core.request.discovery.url.base import UrlDiscoveryPlugin
from core.request.context import RequestContext
from core.request.descriptor import RequestDescriptor
from core.request.downloader.config import ScrapyDownloaderSpec
from core.request.profile import RequestProfile
from core.request.typing import ResponseFormat
from core.runtime import RuntimeContext


class DummyTransformExecutor:
    def transform(self, *, value, configs, context):
        return value


class DummyPipelineExecutor:
    async def execute(self, nodes, selector):
        return None


class DummyUrlDiscoveryPlugin(UrlDiscoveryPlugin[HtmlDiscoveryConfig]):
    async def urls(self, *, response, context, config):
        return None


def test_transform_urls_handles_none():
    plugin = DummyUrlDiscoveryPlugin(
        transform_executor=DummyTransformExecutor(),
        pipeline_executor=DummyPipelineExecutor(),
    )

    descriptor = RequestDescriptor(
        url="https://example.com",
        kind="list",
        target_spider="news",
        profile=RequestProfile(
            downloader=ScrapyDownloaderSpec(),
            response_format=ResponseFormat.HTML,
        ),
        method="GET",
    )
    request = RequestContext(
        descriptor=descriptor,
        configs=[],
        runtime=RuntimeContext(),
    )

    config = HtmlDiscoveryConfig(
        target_spider="news",
        request_kind="list",
        selector={
            "type": "css",
            "selector": "ul.pager a",
            "selection": "single",
            "extract": "attribute",
            "attribute": "href",
        },
    )

    assert plugin.transform_urls(urls=None, request=request, config=config) == []
