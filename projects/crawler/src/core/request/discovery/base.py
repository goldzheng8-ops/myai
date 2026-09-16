from __future__ import annotations

from abc import abstractmethod
from collections.abc import Iterable
from typing import ClassVar, Generic, TypeVar

from core.extraction.response import ResponseAdapter
from core.plugin import Plugin

from core.request.context import RequestContext
from core.request.descriptor import RequestDescriptor

from core.request.discovery.context import DiscoveryContext
from core.request.discovery.exception import DiscoveryError

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
):
    plugin_type: ClassVar[DiscoveryType]

    config_type: ClassVar[type[DiscoveryConfig]]

    @abstractmethod
    async def discover(
        self,
        *,
        context: DiscoveryContext,
        config: ConfigT,
    ) -> DiscoveryResult:
        raise NotImplementedError

    @staticmethod
    def build_record(
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
                self.build_record(descriptor)
                for descriptor in descriptors
            ],
        )

    @staticmethod
    def require_request(
        context: DiscoveryContext,
    ) -> RequestContext:
        if context.request is None:
            raise DiscoveryError(
                "URL discovery requires a request context.",
            )

        return context.request

    @staticmethod
    def require_response(
        context: DiscoveryContext,
    ) -> ResponseAdapter:
        if context.response is None:
            raise DiscoveryError(
                "URL discovery requires a response.",
            )

        return context.response


