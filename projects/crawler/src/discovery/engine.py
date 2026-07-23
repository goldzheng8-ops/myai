

from adapters.base import ResponseAdapter
from config.discovery.base import DiscoveryConfig
from discovery.registry import DiscoveryRegistry
from runtime.discovery_result import DiscoveryResult
from runtime.request_context import RequestContext


class DiscoveryEngine:

    def __init__(
        self,
        registry: DiscoveryRegistry,
    ):
        self._registry = registry


    async def discover(
        self,
        *,
        response: ResponseAdapter,
        context: RequestContext,
        config: DiscoveryConfig,
    ) -> DiscoveryResult:

        plugin = self._registry.get(
            config.type
        )

        if not isinstance(
            config,
            plugin.config_type,
        ):
            raise TypeError(
                f"Invalid config for {config.type}"
            )


        return await plugin.discover(
            response=response,
            context=context,
            config=config,
        )