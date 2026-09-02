from typing import Any
from core.extraction.extractor.executor import ExtractExecutor
from core.extraction.response.factory import ResponseAdapterFactory
from core.request.discovery.engine import DiscoveryEngine
from core.request.middleware.fingerprint import FingerprintProvider
from core.request.runner import RequestRunner
from core.spider.services import SpiderServices
from core.spider.executor import SpiderExecutor
from core.provider import ProviderBuilder, ProviderResolver
from core.spider import (
    SpiderRegistry,
    build_api_spider_factory,
    build_browser_spider_factory,
    build_detail_spider_factory,
    build_list_spider_factory,
    SpiderTemplate,
)


def register_spider_components(
    builder: ProviderBuilder,
) -> None:

    builder.add_factory(
        SpiderExecutor,
        lambda resolver: SpiderExecutor(
            services=resolver.resolve(
                SpiderServices,
            ),
        ),
    )

    builder.add_factory(
        SpiderServices,
        lambda resolver: SpiderServices(
            request_runner=resolver.resolve(RequestRunner),
            extract_engine=resolver.resolve(ExtractExecutor),
            discovery_engine=resolver.resolve(DiscoveryEngine),
            fingerprint_provider=resolver.resolve(FingerprintProvider),
            response_adapter_factory=resolver.resolve(ResponseAdapterFactory),
        ),
    )

    builder.add_factory(
        SpiderRegistry,
        lambda resolver: create_spider_registry(
            resolver,
        ),
    )

def create_spider_registry(
    resolver: ProviderResolver[Any, Any],
) -> SpiderRegistry:

    registry = SpiderRegistry()

  
    registry.register(
        SpiderTemplate.API,
        build_api_spider_factory(
            resolver,
        ),
    )
    registry.register(
        SpiderTemplate.BROWSER,
        build_browser_spider_factory(
            resolver,
        ),
    )
    registry.register(
        SpiderTemplate.DETAIL,
        build_detail_spider_factory(
            resolver,
        ),
    )
    registry.register(
        SpiderTemplate.LIST,
        build_list_spider_factory(
            resolver,
        ),
    )



    return registry