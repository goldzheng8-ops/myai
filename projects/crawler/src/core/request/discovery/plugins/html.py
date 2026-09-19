
from core.extraction.response.base import ResponseAdapter
from core.request.discovery.config import HtmlDiscoveryConfig
from core.request.discovery.typing import DiscoveryType
from core.request.discovery.url.base import UrlDiscoveryPlugin
from core.request.context import RequestContext


class HtmlDiscoveryPlugin(
    UrlDiscoveryPlugin[
        HtmlDiscoveryConfig
    ],
):
    plugin_type = DiscoveryType.HTML
    config_type = HtmlDiscoveryConfig

    async def urls(
        self,
        *,
        response: ResponseAdapter,
        context: RequestContext,
        config: HtmlDiscoveryConfig,
    ) -> list[str]:

        nodes = await response.select(
            config.selector,
        )

        value = await self._pipeline_executor.execute(
            nodes,
            config.selector,
        )
        if isinstance(value, str):
            return [value]
        return value