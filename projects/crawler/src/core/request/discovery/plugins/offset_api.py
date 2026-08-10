from typing import Any

from core.request.response.base import ResponseAdapter





from models.config.discovery.offset_api import OffsetApiConfig
from core.request.discovery.api.base import ApiDiscoveryPlugin
from models.enums.discovery_type import DiscoveryType
from core.request.context import RequestContext

class OffsetApiDiscovery(
    ApiDiscoveryPlugin[OffsetApiConfig]
):

    plugin_type = DiscoveryType.OFFSET_API

    config_type = OffsetApiConfig

    async def variables(
        self,
        *,
        response: ResponseAdapter,
        context: RequestContext,
        config: OffsetApiConfig,
    ) -> dict[str, Any]:

        current = int(
            context.descriptor.params.get(
                config.parameter,
                config.start,
            )
        )

        return {
            "offset": current + config.limit,
        }