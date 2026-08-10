
from abc import ABC
from typing import TypeVar

from core.request.response.base import ResponseAdapter
from core.request.discovery.base import HtmlDiscoveryConfig
from core.request.discovery.url.base import UrlDiscoveryPlugin
from core.request.context import RequestContext


HtmlConfigT = TypeVar(
    "HtmlConfigT",
    bound=HtmlDiscoveryConfig,
)

class HtmlDiscoveryPlugin(
    UrlDiscoveryPlugin[
        HtmlConfigT
    ],
    ABC,
):

    async def urls(
        self,
        *,
        response: ResponseAdapter,
        context: RequestContext,
        config: HtmlConfigT,
    ) -> list[str]:

        value = await response.select(
            config.selector,
        )

        return self.normalize(value)