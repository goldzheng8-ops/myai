from abc import ABC, abstractmethod
from typing import Any, ClassVar, TypeVar

from core.extraction.response.base import ResponseAdapter

from core.request.discovery.config import UrlDiscoveryConfig
from core.request.discovery.base import DiscoveryPlugin
from core.request.typing import RequestKind
from core.request.builder import RequestBuilder
from core.request.descriptor import RequestDescriptor
from core.request.discovery.result import DiscoveryResult
from core.request.context import RequestContext
from core.request.profile import RequestProfile


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
                profile=context.descriptor.profile,
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

        return RequestBuilder.create(
            url=url,
            kind=self.request_kind,
            profile=profile,
        )