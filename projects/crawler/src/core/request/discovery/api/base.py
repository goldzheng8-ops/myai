

from abc import ABC, abstractmethod
from typing import Any, TypeVar

from core.extraction.response.base import ResponseAdapter
from core.request.discovery.config import ApiDiscoveryConfig
from core.request.discovery.base import DiscoveryPlugin
from core.request.discovery.api.patch_renderer import RequestPatchRenderer
from core.request.builder import RequestBuilder
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

        descriptor = RequestBuilder.from_patch(
            descriptor=context.descriptor,
            patch=patch,
        )

        return self.build_result(
            [descriptor]
        )