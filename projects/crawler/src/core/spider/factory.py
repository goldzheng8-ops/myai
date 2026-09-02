from __future__ import annotations

from typing import Any
from collections.abc import Callable
from core.provider import  ProviderResolver
from core.spider.services import SpiderServices
from core.spider.template.base import TemplateSpider
from core.spider.template.api import TemplateApiSpider
from core.spider.template.browser import TemplateBrowserSpider
from core.spider.template.detail import TemplateDetailSpider
from core.spider.template.list import TemplateListSpider


SpiderFactory = Callable[
    [],
    TemplateSpider[Any],
]

def build_api_spider_factory(
    resolver: ProviderResolver[Any, Any],
) -> SpiderFactory:

    def factory() -> TemplateApiSpider:

        return TemplateApiSpider(
            resolver.resolve(
                SpiderServices,
            ),
        )

    return factory

def build_browser_spider_factory(
    resolver: ProviderResolver[Any, Any],
) -> SpiderFactory:

    def factory() -> TemplateBrowserSpider:

        return TemplateBrowserSpider(
            resolver.resolve(
                SpiderServices,
            ),
        )

    return factory

def build_detail_spider_factory(
    resolver: ProviderResolver[Any, Any],
) -> SpiderFactory:

    def factory() -> TemplateDetailSpider:

        return TemplateDetailSpider(
            resolver.resolve(
                SpiderServices,
            ),
        )

    return factory

def build_list_spider_factory(
    resolver: ProviderResolver[Any, Any],
) -> SpiderFactory:

    def factory() -> TemplateListSpider:

        return TemplateListSpider(
            resolver.resolve(
                SpiderServices,
            ),
        )

    return factory