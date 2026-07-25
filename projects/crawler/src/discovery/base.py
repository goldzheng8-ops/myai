from abc import ABC, abstractmethod
from typing import ClassVar, Generic, Iterable, TypeVar


from adapters.base import ResponseAdapter
from enums.discovery_type import DiscoveryType
from registry.plugin_base import Plugin
from runtime.discovery_result import DiscoveryRecord, DiscoveryResult
from runtime.request_context import RequestContext
from runtime.discovery_descriptor import RequestDescriptor
from config.discovery.base import DiscoveryConfig, HtmlDiscoveryConfig


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




