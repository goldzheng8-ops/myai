from abc import ABC, abstractmethod
from typing import  Generic, TypeVar


from adapters.base import ResponseAdapter
from enums.discovery_type import DiscoveryType
from runtime.discovery_result import DiscoveryResult
from runtime.request_context import RequestContext
from config.discovery.base import DiscoveryConfig

ConfigT = TypeVar(
    "ConfigT",
    bound=DiscoveryConfig,
)


class DiscoveryPlugin(
    Generic[ConfigT],
    ABC,
):

    discovery_type: DiscoveryType

    config_type: type[ConfigT]


    @abstractmethod
    async def discover(
        self,
        *,
        response: ResponseAdapter,
        context: RequestContext,
        config: ConfigT,
    ) -> DiscoveryResult:
        ...