from abc import ABC, abstractmethod
from typing import ClassVar
from discovery.config.base import DiscoveryConfig
from discovery.config.enums import DiscoveryType
from discovery.result import DiscoveryResult
from adapters.base import ResponseAdapter
from request.context import RequestContext

class DiscoveryPlugin(ABC):

    type:ClassVar[DiscoveryType]

    @abstractmethod
    async def discover(
        self,
        response: ResponseAdapter,
        request: RequestContext,
        config: DiscoveryConfig,
    ) -> DiscoveryResult:
        ...