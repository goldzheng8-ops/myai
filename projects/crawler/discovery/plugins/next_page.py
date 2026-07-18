

from adapters.base import ResponseAdapter
from discovery.base import DiscoveryPlugin
from discovery.config.base import DiscoveryConfig
from discovery.config.next_page import NextPageConfig
from discovery.result import DiscoveryResult
from request.context import RequestContext



class NextPagePlugin(DiscoveryPlugin):
    async def discover(self, response: ResponseAdapter, request: RequestContext, configs: DiscoveryConfig) -> DiscoveryResult:
        result = DiscoveryResult()
        for config in configs:
            if isinstance(config, NextPageConfig):
                next_page_url = await self.get_next_page_url(response, config)
                if next_page_url:
                    next_request = RequestContext(
                        request=request.request,
                        crawler=request.crawler,
                        meta=request.meta.copy(),
                        downloader=request.downloader,
                    )
                    next_request.request.url = next_page_url
                    result.requests.append(next_request)
        return result
    def get_next_page_url(self, response: ResponseAdapter, config: NextPageConfig) -> str:
        # Implement the logic to extract the next page URL from the response based on the config
        # This is a placeholder implementation and should be replaced with actual logic
        return response.get_next_page_url(config.selector)