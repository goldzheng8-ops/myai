


from typing import Any

from adapters.base import ResponseAdapter
from config.discovery.cursor_api import CursorApiConfig

from discovery.base import ApiDiscoveryPlugin
from enums.discovery_type import DiscoveryType
from runtime.request_context import RequestContext


class CursorApiDiscovery(
    ApiDiscoveryPlugin[CursorApiConfig]
):

    discovery_type = DiscoveryType.CURSOR_API

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