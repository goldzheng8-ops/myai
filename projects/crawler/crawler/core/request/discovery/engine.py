from core.request.discovery.context import DiscoveryContext
from .config import DiscoveryConfigUnion
from core.request.discovery.registry import DiscoveryRegistry
from core.request.discovery.result import DiscoveryResult


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
        context: DiscoveryContext,
        config: DiscoveryConfigUnion,
    ) -> DiscoveryResult:

        plugin = self._registry.create(
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
            context=context,
            config=config,
        )