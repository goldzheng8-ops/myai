from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Iterable
from typing import ClassVar, Generic, TypeVar

from core.plugin import Plugin
from core.request.context import RequestContext
from core.request.descriptor import RequestDescriptor

from core.extraction.response import ResponseAdapter

from .config import DiscoveryConfig
from .result import DiscoveryRecord, DiscoveryResult
from .typing import DiscoveryType


ConfigT = TypeVar(
    "ConfigT",
    bound=DiscoveryConfig,
)


class DiscoveryPlugin(
    Plugin,
    Generic[ConfigT],
    ABC,
):

    type: ClassVar[DiscoveryType]

    config_type: ClassVar[type[DiscoveryConfig]]

    @abstractmethod
    async def discover(
        self,
        *,
        response: ResponseAdapter,
        context: RequestContext,
        config: ConfigT,
    ) -> DiscoveryResult:
        raise NotImplementedError

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
            records=[
                self.build_record(
                    descriptor
                )
                for descriptor in descriptors
            ]
        )




