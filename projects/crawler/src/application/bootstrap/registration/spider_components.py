from typing import Any

from application.config.registry import SpiderConfigRegistry
from core.extraction.extractor.executor import ExtractExecutor
from core.output.engine import OutputEngine
from core.request.discovery.engine import DiscoveryEngine
from core.request.middleware.fingerprint.provider import FingerprintProvider
from core.request.runner import RequestRunner
from core.runtime import RuntimeContext
from core.spider.handler.download_request import DownloadRequestHandler
from core.spider.handler.spider_request import SpiderRequestHandler
from core.spider.registry import SpiderRegistry
from core.spider.services import SpiderServices
from core.provider import ProviderBuilder, ProviderResolver
from core.spider.factory import (
    build_download_template_factory,
    build_extraction_template_factory,
    build_plain_template_factory
)
from core.spider.typing import SpiderTemplate


def register_spider_components(
    builder: ProviderBuilder,
) -> None:
    
    builder.add_type(RuntimeContext)


    builder.add_factory(
        SpiderRequestHandler,
        lambda resolver: SpiderRequestHandler(
            services=resolver.resolve(SpiderServices),
            spider_registry=resolver.resolve(SpiderRegistry),
            spider_config_registry=resolver.resolve(SpiderConfigRegistry),
            runtime=resolver.resolve(RuntimeContext),
        ),
    )

    builder.add_factory(
        DownloadRequestHandler,
        lambda resolver: DownloadRequestHandler(
            services=resolver.resolve(SpiderServices),
            spider_registry=resolver.resolve(SpiderRegistry),
            spider_config_registry=resolver.resolve(SpiderConfigRegistry),
            runtime=resolver.resolve(RuntimeContext),
        ),
    )

    builder.add_factory(
        SpiderServices,
        lambda resolver: SpiderServices(
            request_runner=resolver.resolve(RequestRunner),
            extract_executor=resolver.resolve(ExtractExecutor),
            discovery_engine=resolver.resolve(DiscoveryEngine),
            fingerprint_provider=resolver.resolve(FingerprintProvider),
            output_engine=resolver.resolve(OutputEngine),
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
        SpiderTemplate.EXTRACTION,
        build_extraction_template_factory(
            resolver,
        ),
    )
    registry.register(
        SpiderTemplate.DOWNLOAD,
        build_download_template_factory(
            resolver,
        ),
    )
    registry.register(
        SpiderTemplate.PLAIN,
        build_plain_template_factory(
            resolver,
        ),
    )




    return registry