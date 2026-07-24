from abc import ABC, abstractmethod
from typing import  Any, ClassVar, Generic, Iterable, TypeVar


from adapters.base import ResponseAdapter
from discovery.patch_renderer import RequestPatchRenderer
from enums.discovery_type import DiscoveryType
from enums.request_kind import RequestKind
from request.descriptor_factory import RequestDescriptorFactory
from runtime.discovery_result import DiscoveryRecord, DiscoveryResult
from runtime.request_context import RequestContext
from runtime.discovery_descriptor import RequestDescriptor
from config.discovery.base import ApiDiscoveryConfig, DiscoveryConfig, HtmlDiscoveryConfig
from runtime.request_profile import RequestProfile

ConfigT = TypeVar(
    "ConfigT",
    bound=DiscoveryConfig,
)
ApiConfigT = TypeVar(
    "ApiConfigT",
    bound=ApiDiscoveryConfig,
)

HtmlConfigT = TypeVar(
    "HtmlConfigT",
    bound=HtmlDiscoveryConfig,
)


class DiscoveryPlugin(
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

class ApiDiscoveryPlugin(
    DiscoveryPlugin[ApiConfigT],
    ABC,
):

    @abstractmethod
    async def variables(
        self,
        *,
        response: ResponseAdapter,
        context: RequestContext,
        config: ApiConfigT,
    ) -> dict[str, Any] | None:
        """
        返回 Patch 模板需要的变量。

        None 表示没有发现下一页。
        """


    async def discover(
        self,
        *,
        response: ResponseAdapter,
        context: RequestContext,
        config: ApiConfigT,
    ) -> DiscoveryResult:

        variables = await self.variables(
            response=response,
            context=context,
            config=config,
        )

        if variables is None:
            return DiscoveryResult()

        patch = RequestPatchRenderer.render(
            config.patch,
            **variables,
        )

        descriptor = (
            RequestDescriptorFactory.api_from_patch(
                context=context,
                patch=patch,
            )
        )

        return self.build_result(
            [descriptor]
        )


class HtmlDiscoveryPlugin(
    DiscoveryPlugin[HtmlConfigT],
    ABC,
):

    request_kind: ClassVar[RequestKind]

    async def discover(
        self,
        *,
        response: ResponseAdapter,
        context: RequestContext,
        config: HtmlConfigT,
    ) -> DiscoveryResult:

        urls = await self.extract_urls(
            response=response,
            config=config,
        )

        descriptors = [

            self.build_descriptor(
                url=url,
                profile=config.profile,
            )

            for url in urls
        ]

        return self.build_result(
            descriptors
        )

    async def extract_urls(
        self,
        *,
        response: ResponseAdapter,
        config: HtmlConfigT,
    ) -> list[str]:

        value = await response.select(
            config.selector,
        )

        return self.normalize_urls(
            value
        )

    @staticmethod
    def normalize_urls(
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