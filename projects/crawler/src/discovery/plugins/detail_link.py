

from discovery.base import DiscoveryPlugin
from discovery.config.enums import DiscoveryType
from discovery.delta import DiscoveryItem
from discovery.result import DiscoveryResult


class DetailPlugin(DiscoveryPlugin):

    type = DiscoveryType.DETAIL_LINK

    async def discover(
        self,
        response: ResponseAdapter,
        request: RequestContext,
        config: DiscoveryConfig,
    ) -> DiscoveryResult:

        urls = ...

        return DiscoveryResult(
            items=[
                DiscoveryItem(
                    type=self.type,
                    url=url,
                )
                for url in urls
            ]
        )