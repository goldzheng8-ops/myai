

from abc import ABC, abstractmethod
from typing import Any, TypeVar

from core.response.base import ResponseAdapter
from models.config.discovery.base import ApiDiscoveryConfig
from discovery.base import DiscoveryPlugin
from discovery.api.patch_renderer import RequestPatchRenderer
from models.runtime.request.factory import RequestDescriptorFactory
from models.runtime.discovery_result import DiscoveryResult
from models.runtime.request_context import RequestContext


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

        descriptor = (
            RequestDescriptorFactory.api_from_patch(
                context=context,
                patch=patch,
            )
        )

        return self.build_result(
            [descriptor]
        )