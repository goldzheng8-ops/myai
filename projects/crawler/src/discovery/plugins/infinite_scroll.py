from typing import Any

from adapters.base import ResponseAdapter


from config.discovery.infinite_scroll import InfiniteScrollConfig
from discovery.base import ApiDiscoveryPlugin
from enums.discovery_type import DiscoveryType
from runtime.request_context import RequestContext

class InfiniteScrollDiscovery(
    ApiDiscoveryPlugin[InfiniteScrollConfig]
):

    discovery_type = DiscoveryType.INFINITE_SCROLL

    config_type = InfiniteScrollConfig

    async def variables(
        self,
        *,
        response: ResponseAdapter,
        context: RequestContext,
        config: InfiniteScrollConfig,
    ) -> dict[str, Any] | None:

        await response.scroll(
            count=config.scroll_count,
            delay=config.scroll_delay,
        )

        cursor = await response.select(
            config.selector,
        )

        if cursor is None:
            return None

        return {
            "cursor": cursor,
        }