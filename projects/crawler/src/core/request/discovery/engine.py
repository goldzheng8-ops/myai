

from core.extraction.response.base import ResponseAdapter
from .config import DiscoveryConfig
from core.request.discovery.registry import DiscoveryRegistry
from core.request.discovery.result import DiscoveryResult
from core.request.context import RequestContext


class DiscoveryEngine:

    def __init__(
        self,
        registry: DiscoveryRegistry,
    ) -> None:

        self._registry = registry

    @property
    def registry(
        self,
    ) -> DiscoveryRegistry:

        return self._registry

    async def discover(
        self,
        *,
        response: ResponseAdapter,
        context: RequestContext,
        config: DiscoveryConfig,
    ) -> DiscoveryResult:

        plugin = self._registry.get(
            config.type,
        )

        if not isinstance(
            config,
            plugin.config_type,
        ):
            raise TypeError(
                f"Invalid config for "
                f"{config.type}: "
                f"expected {plugin.config_type.__name__}, "
                f"got {type(config).__name__}",
            )

        return await plugin.discover(
            response=response,
            context=context,
            config=config,
        )