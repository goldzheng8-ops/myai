from abc import abstractmethod
from collections.abc import Iterable
from typing import Any, TypeVar

from core.extraction.response.base import ResponseAdapter

from core.extraction.selector.executor import PipelineExecutor
from core.extraction.transform.context import TransformContext
from core.extraction.transform.executor import TransformExecutor
from core.request.discovery.config import UrlDiscoveryConfig
from core.request.discovery.base import DiscoveryPlugin
from core.request.discovery.context import DiscoveryContext
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
):

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
    ) -> Iterable[str]:
        raise NotImplementedError

    async def discover(
        self,
        *,
        context: DiscoveryContext,
        config: UrlConfigT,
    ) -> DiscoveryResult:
        request = self.require_request(context)
        response = self.require_response(context)
        urls = await self.urls(
            response=response,
            context=request,
            config=config,
        )
        transformed_urls = self.transform_urls(
            urls=urls,
            request=request,
            config=config,
        )
        descriptors = self.build_descriptors(
            urls=transformed_urls,
            request=request,
            config=config,
        )

        return self.build_result(descriptors)

    def transform_urls(
        self,
        *,
        urls: Iterable[str] | None,
        request: RequestContext,
        config: UrlConfigT,
    ) -> list[str]:

        if urls is None:
            return []

        transform_context = TransformContext(
            request=request,
        )

        result: list[str] = []

        for url in urls:
            value = self._transform_executor.transform(
                value=url,
                configs=config.transforms,
                context=transform_context,
            )

            result.extend(
                self.normalize(value),
            )

        return result

    def build_descriptors(
        self,
        *,
        urls: Iterable[str],
        request: RequestContext,
        config: UrlConfigT,
    ) -> list[RequestDescriptor]:

        profile = request.descriptor.profile

        return [
            self.build_descriptor(
                url=url,
                profile=profile,
                config=config,
            )
            for url in urls
        ]

    def build_descriptor(
        self,
        *,
        url: str,
        profile: RequestProfile,
        config: UrlConfigT,
    ) -> RequestDescriptor:

        return RequestBuilder.create(
            url=url,
            kind=config.request_kind,
            profile=profile,
            target_spider=config.target_spider,
        )

    @staticmethod
    def normalize(
        value: Any,
    ) -> list[str]:

        if value is None:
            return []

        if isinstance(value, str):
            values: Iterable[Any] = (value,)

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