from typing import Any

from core.extraction.response.base import ResponseAdapter


from core.request.discovery.config import InfiniteScrollConfig

from core.request.discovery.api.base import ApiDiscoveryPlugin
from core.request.discovery.typing import DiscoveryType
from core.request.context import RequestContext

class InfiniteScrollDiscovery(
    ApiDiscoveryPlugin[InfiniteScrollConfig]
):

    type = DiscoveryType.INFINITE_SCROLL

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