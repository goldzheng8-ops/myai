

from discovery.config.base import DiscoveryConfig
from discovery.registry import DiscoveryRegistry
from discovery.result import DiscoveryResult, RequestContext
from adapters.base import ResponseAdapter




class DiscoveryEngine:

    def __init__(
        self,
        registry: DiscoveryRegistry,
    ):
        self._registry = registry

    async def discover(
        self,
        response: ResponseAdapter,
        request: RequestContext,
        configs: list[DiscoveryConfig],
    ) -> DiscoveryResult:

        result = DiscoveryResult()

        for config in configs:

            plugin = self._registry.get(config.type)

            discovery = await plugin.discover(
                response,
                request,
                config,
            )

            result.requests.extend(discovery.requests)

        return result