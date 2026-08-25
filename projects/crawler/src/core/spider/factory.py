from __future__ import annotations

from typing import Any, Callable

from core.provider import  ProviderResolver
from core.spider.services import SpiderServices
from core.spider.template import TemplateSpider


SpiderFactory = Callable[
    [],
    TemplateSpider[Any],
]

def build_spider_factory(
    resolver: ProviderResolver[Any, Any],
    spider_type: type[TemplateSpider[Any]],
) -> SpiderFactory:

    def factory() -> TemplateSpider[Any]:

        return spider_type(
            resolver.resolve(
                SpiderServices,
            ),
        )

    return factory