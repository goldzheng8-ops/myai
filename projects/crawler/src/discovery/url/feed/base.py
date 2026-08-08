
from abc import ABC
from functools import cached_property
from typing import ClassVar, TypeVar

from core.response.base import ResponseAdapter
from models.config.discovery.base import FeedDiscoveryConfig
from discovery.parser.base import FeedParser
from discovery.url.base import UrlDiscoveryPlugin

from models.runtime.request_context import RequestContext


FeedConfigT = TypeVar(
    "FeedConfigT",
    bound=FeedDiscoveryConfig,
)

class FeedDiscoveryPlugin(
    UrlDiscoveryPlugin[
        FeedConfigT
    ],
    ABC,
):
    parser_cls : ClassVar[type[FeedParser]]

    @cached_property
    def parser(self) -> FeedParser:
        return self.parser_cls()
    
    async def urls(
        self,
        *,
        response: ResponseAdapter,
        context: RequestContext,
        config: FeedConfigT,
    ) -> list[str]:

        xml = await response.xml()

        return self.parser.parse(
            xml
        )