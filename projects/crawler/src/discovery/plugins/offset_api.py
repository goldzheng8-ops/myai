from typing import Any

from adapters.base import ResponseAdapter



from config.discovery.offset_api import OffsetApiConfig
from discovery.base import ApiDiscoveryPlugin
from enums.discovery_type import DiscoveryType
from runtime.request_context import RequestContext

class OffsetApiDiscovery(
    ApiDiscoveryPlugin[OffsetApiConfig]
):

    discovery_type = DiscoveryType.OFFSET_API

    config_type = OffsetApiConfig

    async def variables(
        self,
        *,
        response: ResponseAdapter,
        context: RequestContext,
        config: OffsetApiConfig,
    ) -> dict[str, Any]:

        current = int(
            context.request.params.get(
                config.parameter,
                config.start,
            )
        )

        return {
            "offset": current + config.limit,
        }