


from typing import Any

from core.extraction.response.base import ResponseAdapter
from core.request.discovery.config import CursorApiConfig


from core.request.discovery.api.base import ApiDiscoveryPlugin
from core.request.discovery.typing import DiscoveryType
from core.request.context import RequestContext


class CursorApiDiscovery(
    ApiDiscoveryPlugin[CursorApiConfig]
):

    plugin_type = DiscoveryType.CURSOR_API

    config_type = CursorApiConfig

    async def variables(
        self,
        *,
        response: ResponseAdapter,
        context: RequestContext,
        config: CursorApiConfig,
    ) -> dict[str, Any] | None:

        cursor = await response.select(
            config.selector,
        )

        if cursor is None:
            return None

        return {
            "cursor": cursor,
        }