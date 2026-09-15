from __future__ import annotations

from typing import Any
from collections.abc import Callable
from core.provider import  ProviderResolver
from core.spider.services import SpiderServices
from core.spider.template.base import RequestTemplate
from core.spider.template.api import ApiRequestTemplate
from core.spider.template.browser import BrowserRequestTemplate
from core.spider.template.detail import DetailRequestTemplate
from core.spider.template.list import ListRequestTemplate


SpiderFactory = Callable[
    [],
    RequestTemplate[Any],
]

def build_api_spider_factory(
    resolver: ProviderResolver[Any, Any],
) -> SpiderFactory:

    def factory() -> ApiRequestTemplate:

        return ApiRequestTemplate(
            resolver.resolve(
                SpiderServices,
            ),
        )

    return factory

def build_browser_spider_factory(
    resolver: ProviderResolver[Any, Any],
) -> SpiderFactory:

    def factory() -> BrowserRequestTemplate:

        return BrowserRequestTemplate(
            resolver.resolve(
                SpiderServices,
            ),
        )

    return factory

def build_detail_spider_factory(
    resolver: ProviderResolver[Any, Any],
) -> SpiderFactory:

    def factory() -> DetailRequestTemplate:

        return DetailRequestTemplate(
            resolver.resolve(
                SpiderServices,
            ),
        )

    return factory

def build_list_spider_factory(
    resolver: ProviderResolver[Any, Any],
) -> SpiderFactory:

    def factory() -> ListRequestTemplate:

        return ListRequestTemplate(
            resolver.resolve(
                SpiderServices,
            ),
        )

    return factory