from abc import ABC, abstractmethod
from typing import Any, ClassVar, TypeVar

from adapters.base import ResponseAdapter

from config.discovery.base import UrlDiscoveryConfig
from discovery.base import DiscoveryPlugin
from enums.request_kind import RequestKind
from request.descriptor_factory import RequestDescriptorFactory
from runtime.discovery_descriptor import RequestDescriptor
from runtime.discovery_result import DiscoveryResult
from runtime.request_context import RequestContext
from runtime.request_profile import RequestProfile


UrlConfigT = TypeVar(
    "UrlConfigT",
    bound=UrlDiscoveryConfig,
)

class UrlDiscoveryPlugin(
    DiscoveryPlugin[UrlConfigT],
    ABC,
):

    request_kind: ClassVar[RequestKind]

    @abstractmethod
    async def urls(
        self,
        *,
        response: ResponseAdapter,
        context: RequestContext,
        config: UrlConfigT,
    ) -> list[str]:
        ...

    async def discover(
        self,
        *,
        response: ResponseAdapter,
        context: RequestContext,
        config: UrlConfigT,
    ) -> DiscoveryResult:

        urls = await self.urls(
            response=response,
            context=context,
            config=config,
        )

        descriptors = [
            self.build_descriptor(
                url=url,
                profile=config.profile,
            )
            for url in urls
        ]

        return self.build_result(descriptors)

    @staticmethod
    def normalize(
        value: Any,
    ) -> list[str]:

        if value is None:
            return []

        if isinstance(value, str):
            return [value]

        return [
            str(item)
            for item in value
            if item is not None
        ]
    def build_descriptor(
        self,
        *,
        url: str,
        profile: RequestProfile,
    ) -> RequestDescriptor:

        return RequestDescriptorFactory.create(
            url=url,
            kind=self.request_kind,
            profile=profile,
        )
