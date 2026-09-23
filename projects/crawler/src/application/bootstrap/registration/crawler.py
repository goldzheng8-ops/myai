
from typing import Any

from application.config.model import ApplicationConfig
from application.crawler.application import CrawlerApplication
from application.crawler.service import CrawlerService
from core.lifecycle.manager import LifecycleManager
from core.output.engine import OutputEngine
from core.provider import ProviderBuilder, ProviderResolver
from core.request.middleware.fingerprint.provider import FingerprintProvider
from core.spider.dispatcher import RequestKindDispatcher
from core.spider.executor import CrawlerExecutor
from core.spider.handler.download_request import DownloadRequestHandler
from core.spider.handler.base import RequestKindHandler
from core.spider.handler.registry import RequestKindHandlerRegistry
from core.spider.handler.search import SearchRequestHandler
from core.spider.handler.spider_request import SpiderRequestHandler
from core.spider.runner import CrawlerRunner
from application.config.registry import SpiderConfigRegistry
from application.config.resolver import SpiderConfigResolver

def register_request_dispatcher(
    builder: ProviderBuilder,
) -> None:


    builder.add_factory(
        RequestKindHandlerRegistry,
        lambda resolver: create_request_kind_handler_registry(
            resolver,
        ),
    )

    builder.add_factory(
        RequestKindDispatcher,
        lambda resolver: RequestKindDispatcher(
            registry=resolver.resolve(
                RequestKindHandlerRegistry,
            ),
        ),
    )

def create_request_kind_handler_registry(
    resolver: ProviderResolver[Any, Any],
) -> RequestKindHandlerRegistry:

    registry = RequestKindHandlerRegistry()

    handlers: tuple[RequestKindHandler, ...] = (
        resolver.resolve(SpiderRequestHandler),
        resolver.resolve(DownloadRequestHandler),
        resolver.resolve(SearchRequestHandler),
    )

    for handler in handlers:
        for kind in handler.kinds:
            registry.register(
                kind,
                handler,
            )

    return registry

def register_crawler(
    builder: ProviderBuilder,
    config: ApplicationConfig,
) -> None:

    builder.add_factory(
        CrawlerExecutor,
        lambda resolver: CrawlerExecutor(
            dispatcher=resolver.resolve(
                RequestKindDispatcher,
            ),
            fingerprint_provider=resolver.resolve(
                FingerprintProvider,
            ),
            output_engine=resolver.resolve(
                OutputEngine,
            ),
        ),
    )

    builder.add_factory(
        CrawlerRunner,
        lambda resolver: CrawlerRunner(
            executor=resolver.resolve(
                CrawlerExecutor,
            ),
        ),
    )

    builder.add_factory(
        CrawlerService,
        lambda resolver: CrawlerService(
            runner=resolver.resolve(
                CrawlerRunner,
            ),
            registry=resolver.resolve(
                SpiderConfigRegistry,
            ),
            resolver=resolver.resolve(
                SpiderConfigResolver,
            ),
        ),
    )

    builder.add_factory(
        CrawlerApplication,
        lambda resolver: CrawlerApplication(
            service=resolver.resolve(
                CrawlerService,
            ),
            lifecycle=resolver.resolve(
                LifecycleManager,
            ),
            crawl_config=config.crawl,
        ),
    )