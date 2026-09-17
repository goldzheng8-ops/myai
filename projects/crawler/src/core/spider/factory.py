from __future__ import annotations

from typing import Any
from collections.abc import Callable
from core.provider import  ProviderResolver
from core.spider.services import SpiderServices
from core.spider.template.extraction import RequestTemplate
from core.spider.template.download import DownloadRequestTemplate
from core.spider.template.plain import PlainRequestTemplate
from core.spider.template.extraction import ExtractionRequestTemplate


SpiderFactory = Callable[
    [],
    RequestTemplate[Any],
]

def build_extraction_template_factory(
    resolver: ProviderResolver[Any, Any],
) -> SpiderFactory:

    def factory() -> ExtractionRequestTemplate:

        return ExtractionRequestTemplate(
            resolver.resolve(
                SpiderServices,
            ),
        )

    return factory

def build_plain_template_factory(
    resolver: ProviderResolver[Any, Any],
) -> SpiderFactory:

    def factory() -> PlainRequestTemplate:

        return PlainRequestTemplate(
            resolver.resolve(
                SpiderServices,
            ),
        )

    return factory

def build_download_template_factory(
    resolver: ProviderResolver[Any, Any],
) -> SpiderFactory:

    def factory() -> DownloadRequestTemplate:

        return DownloadRequestTemplate(
            resolver.resolve(
                SpiderServices,
            ),
        )

    return factory

