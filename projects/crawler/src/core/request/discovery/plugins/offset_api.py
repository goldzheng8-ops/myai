from typing import Any

from core.extraction.response.base import ResponseAdapter





from core.request.discovery.config import OffsetApiConfig
from core.request.discovery.api.base import ApiDiscoveryPlugin
from core.request.discovery.typing import DiscoveryType
from core.request.context import RequestContext

class OffsetApiDiscovery(
    ApiDiscoveryPlugin[OffsetApiConfig]
):

    type = DiscoveryType.OFFSET_API

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