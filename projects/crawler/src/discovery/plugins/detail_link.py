


from adapters.base import ResponseAdapter
from config.discovery.detail_link import DetailLinkConfig
from discovery.base import DiscoveryPlugin
from enums.discovery_type import DiscoveryType
from request.descriptor_factory import RequestDescriptorFactory
from runtime.discovery_result import DiscoveryResult
from runtime.request_context import RequestContext

class DetailLinkDiscovery(
    DiscoveryPlugin[DetailLinkConfig]
):

    discovery_type = (
        DiscoveryType.DETAIL_LINK
    )

    config_type = DetailLinkConfig

    def __init__(
        self,
        factory: RequestDescriptorFactory,
    ):
        self.factory = factory


    async def discover(
        self,
        *,
        response: ResponseAdapter,
        context: RequestContext,
        config: DetailLinkConfig,
    ) -> DiscoveryResult:


        urls = await response.css(
            config.selector
        )


        result = DiscoveryResult()


        for url in urls:

            descriptor = (
                self.factory.detail(
                    url=url,
                    profile=context.profile,
                )
            )

            result.requests.append(
                descriptor
            )


        return result