from abc import ABC, abstractmethod
from typing import ClassVar, Generic, Iterable, TypeVar


from core.request.response.base import ResponseAdapter
from models.enums.discovery_type import DiscoveryType
from core.plugin.base import Plugin
from models.runtime.discovery_result import DiscoveryRecord, DiscoveryResult
from core.request.context import RequestContext
from core.request.descriptor import RequestDescriptor
from models.config.discovery.base import DiscoveryConfig, HtmlDiscoveryConfig


ConfigT = TypeVar(
    "ConfigT",
    bound=DiscoveryConfig,
)


HtmlConfigT = TypeVar(
    "HtmlConfigT",
    bound=HtmlDiscoveryConfig,
)


class DiscoveryPlugin(
    Plugin,
    Generic[ConfigT],
    ABC,
):

    plugin_type: ClassVar[DiscoveryType]

    config_type: ClassVar[type[DiscoveryConfig]]

    @abstractmethod
    async def discover(
        self,
        *,
        response: ResponseAdapter,
        context: RequestContext,
        config: ConfigT,
    ) -> DiscoveryResult:
        ...

    def build_record(
        self,
        descriptor: RequestDescriptor,
    ) -> DiscoveryRecord:

        return DiscoveryRecord(
            descriptor=descriptor,
        )

    def build_result(
        self,
        descriptors: Iterable[RequestDescriptor],
    ) -> DiscoveryResult:

        return DiscoveryResult(
            descriptors=[
                self.build_record(
                    descriptor
                )
                for descriptor in descriptors
            ]
        )




