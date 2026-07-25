
from abc import ABC
from typing import TypeVar

from adapters.base import ResponseAdapter
from discovery.base import HtmlDiscoveryConfig
from discovery.url.base import UrlDiscoveryPlugin
from runtime.request_context import RequestContext


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