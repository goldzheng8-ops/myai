from abc import ABC, abstractmethod
from collections.abc import Iterable
from typing import Any, ClassVar, TypeVar

from core.extraction.response.base import ResponseAdapter

from core.extraction.selector.executor import PipelineExecutor
from core.extraction.transform.executor import TransformExecutor
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
    def __init__(
        self,
        transform_executor: TransformExecutor,
        pipeline_executor: PipelineExecutor,
    ) -> None:
        self._transform_executor = transform_executor
        self._pipeline_executor = pipeline_executor

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
        transformed_urls = [
            self._transform_executor.transform(
                url,
                config.transforms,
            )
            for url in urls
        ]
        descriptors = [
            self.build_descriptor(
                url=url,
                profile=context.descriptor.profile,
                target_spider=config.target_spider,
            )
            for url in transformed_urls
        ]

        return self.build_result(descriptors)

    @staticmethod
    def normalize(value: Any) -> list[str]:
        if value is None:
            return []

        if isinstance(value, str):
            values = (value,)
        elif isinstance(value, Iterable):
            values = value
        else:
            return []

        return [
            item.strip()
            for item in values
            if isinstance(item, str)
            and item.strip()
        ]

    def build_descriptor(
        self,
        *,
        url: str,
        profile: RequestProfile,
        target_spider: str,
    ) -> RequestDescriptor:

        return RequestBuilder.create(
            url=url,
            kind=self.request_kind,
            profile=profile,
            target_spider=target_spider,
        )