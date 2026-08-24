from __future__ import annotations

from typing import Any

from core.provider import  Resolver
from core.spider.services import SpiderServices
from core.spider.template import TemplateSpider



class SpiderFactory:
    """
    Creates spider instances through the application resolver.
    """

    def __init__(
        self,
        resolver: Resolver[Any, Any],
    ) -> None:
        self._resolver = resolver

    def create(
        self,
        spider_type: type[TemplateSpider[Any]],
    ) -> TemplateSpider[Any]:

        services = self._resolver.resolve(
            SpiderServices,
        )

        return spider_type(
            services,
        )