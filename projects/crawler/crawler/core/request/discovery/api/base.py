

from abc import ABC, abstractmethod
from dataclasses import replace
from typing import Any, TypeVar

from core.extraction.response.base import ResponseAdapter
from core.request.discovery.config import ApiDiscoveryConfig
from core.request.discovery.base import DiscoveryPlugin
from core.request.discovery.api.patch_renderer import RequestPatchRenderer
from core.request.builder import RequestBuilder
from core.request.discovery.context import DiscoveryContext
from core.request.discovery.result import DiscoveryResult
from core.request.context import RequestContext


ApiConfigT = TypeVar(
    "ApiConfigT",
    bound=ApiDiscoveryConfig,
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
        request: RequestContext,
        config: ApiConfigT,
    ) -> dict[str, Any] | None:
        """
        返回 Patch 模板需要的变量。

        None 表示没有发现下一页。
        """


    async def discover(
        self,
        *,
        context: DiscoveryContext,
        config: ApiConfigT,
    ) -> DiscoveryResult:
        request = self.require_request(context)
        response = self.require_response(context)
        variables = await self.variables(
            response=response,
            request=request,
            config=config,
        )

        if variables is None:
            return DiscoveryResult()

        patch = RequestPatchRenderer.render(
            config.patch,
            **variables,
        )

        descriptor = RequestBuilder.from_patch(
            descriptor=request.descriptor,
            patch=patch,
        )
        
        descriptor = replace(
            descriptor,
            target_spider=config.target_spider,
        )
        
        descriptor = replace(
            descriptor,
            kind=config.request_kind,
        )

        return self.build_result(
            [descriptor]
        )