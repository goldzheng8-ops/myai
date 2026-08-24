from __future__ import annotations
from typing import Any

from application.crawler.application import CrawlerApplication
from application.crawler.service import CrawlerService
from core.spider.factory import SpiderFactory
from application.spider.registry import SpiderRegistry
from core.cache import MemoryCache
from core.cache.protocol import Cache
from core.event import EventDispatcher, EventRegistry
from core.extraction.extractor.engine import ExtractEngine
from core.extraction.response.factory import ResponseAdapterFactory
from core.lifecycle.manager import LifecycleManager
from core.provider import (
    ProviderBuilder,
    Resolver,
    SingletonProvider,
)

from application.config.model import ApplicationConfig
from core.request.discovery.engine import DiscoveryEngine
from core.request.downloader.config import HttpxDownloaderConfig, ScrapyDownloaderConfig,PlaywrightDownloaderConfig
from core.request.downloader.factory import DownloaderFactory
from core.request.downloader.httpx import HttpxDownloader
from core.request.downloader.manager import DownloaderManager
from core.request.downloader.playwright import PlaywrightDownloader
from core.request.downloader.registry import DownloaderRegistry
from core.request.downloader.scrapy.bridge import ScrapyRequestBridge
from core.request.downloader.scrapy.executor import DefaultScrapyRequestExecutor, ScrapyRequestExecutor
from core.request.downloader.scrapy.runner import AsyncCrawlerRunner, ScrapyAsyncCrawlerRunner
from core.request.downloader.scrapy.runtime import DefaultScrapyRuntime, ScrapyRuntime
from core.request.downloader.scrapy.downloader import ScrapyDownloader
from core.request.executor import RequestExecutor
from core.request.executor.downloader import DownloaderRequestExecutor
from core.request.middleware import AuthMiddleware, CacheMiddleware, CookieMiddleware, DeduplicateMiddleware, FingerprintMiddleware, MiddlewareManager, ProxyMiddleware, RetryMiddleware, SessionMiddleware, ThrottleMiddleware
from core.request.middleware.auth.basic import BasicAuthProvider
from core.request.middleware.auth.policy import AuthPolicy
from core.request.middleware.auth.provider import AuthProvider
from core.request.middleware.cache.key import CacheKeyProvider, FingerprintCacheKeyProvider
from core.request.middleware.cache.policy import CachePolicy
from core.request.middleware.config import MiddlewareConfig
from core.request.middleware.cookie.policy import CookiePolicy
from core.request.middleware.deduplicate import DeduplicatePolicy
from core.request.middleware.factory import MiddlewareFactory
from core.request.middleware.fingerprint import DefaultFingerprintProvider, FingerprintProvider
from core.request.middleware.proxy.policy import ProxyPolicy
from core.request.middleware.proxy.provider import ProxyProvider
from core.request.middleware.registry import MiddlewareRegistry
from core.request.middleware.retry.policy import RetryPolicy
from core.request.middleware.session.policy import SessionPolicy
from core.request.middleware.session.store import MemorySessionStore, SessionStore
from core.request.middleware.throttle.limiter import InMemoryThrottleLimiter, ThrottleLimiter
from core.request.middleware.throttle.policy import ThrottlePolicy
from core.request.middleware.throttle.resolver import HostThrottleKeyResolver, ThrottleKeyResolver
from core.request.middleware.typing import MiddlewareType
from core.request.runner import RequestRunner
from core.request.typing import DownloaderType
from core.spider.executor import SpiderExecutor
from core.spider.runner import CrawlerRunner
from core.spider.services import SpiderServices

from .container import ApplicationContainer

def create_httpx_downloader(
    config: HttpxDownloaderConfig | None = None,
) -> HttpxDownloader:
    return HttpxDownloader(
        config=config,
    )

def create_playwright_downloader(
    config: PlaywrightDownloaderConfig | None = None,
) -> PlaywrightDownloader:
    return PlaywrightDownloader(
        config=config,
    )
def build_scrapy_downloader_factory(
    resolver: Resolver[Any, Any],
) -> DownloaderFactory[ScrapyDownloaderConfig]:

    def factory(
        config: ScrapyDownloaderConfig | None = None,
    ) -> ScrapyDownloader:
        return ScrapyDownloader(
            executor=resolver.resolve(
                ScrapyRequestExecutor,
            ),
            bridge=resolver.resolve(
                ScrapyRequestBridge,
            ),
            config=config,
        )

    return factory

def build_auth_middleware_factory(
    resolver: Resolver[Any, Any],
) -> MiddlewareFactory:

    def factory(
        config: MiddlewareConfig | None = None,
    ) -> AuthMiddleware:

        return AuthMiddleware(
            provider=resolver.resolve(
                AuthProvider,
            ),
            policy=resolver.resolve(
                AuthPolicy,
            ),
            config=config,
        )

    return factory
def build_cache_middleware_factory(
    resolver: Resolver[Any, Any],
) -> MiddlewareFactory:

    def factory(
        config: MiddlewareConfig | None = None,
    ) -> CacheMiddleware:

        return CacheMiddleware(
            cache=resolver.resolve(
                Cache,
            ),
            policy=resolver.resolve(
                CachePolicy,
            ),
            key_provider=resolver.resolve(
                CacheKeyProvider,
            ),
            config=config,
        )

    return factory
def build_cookie_middleware_factory(
    resolver: Resolver[Any, Any],
) -> MiddlewareFactory:

    def factory(
        config: MiddlewareConfig | None = None,
    ) -> CookieMiddleware:

        return CookieMiddleware(
            policy=resolver.resolve(
                CookiePolicy,
            ),
            config=config,
        )

    return factory
def build_deduplicate_middleware_factory(
    resolver: Resolver[Any, Any],
) -> MiddlewareFactory:

    def factory(
        config: MiddlewareConfig | None = None,
    ) -> DeduplicateMiddleware:

        return DeduplicateMiddleware(
            policy=resolver.resolve(
                DeduplicatePolicy,
            ),
            config=config,
        )

    return factory

def build_fingerprint_middleware_factory(
    resolver: Resolver[Any, Any],
) -> MiddlewareFactory:

    def factory(
        config: MiddlewareConfig | None = None,
    ) -> FingerprintMiddleware:

        return FingerprintMiddleware(
            provider=resolver.resolve(
                FingerprintProvider,
            ),
            config=config,
        )

    return factory
def build_proxy_middleware_factory(
    resolver: Resolver[Any, Any],
) -> MiddlewareFactory:

    def factory(
        config: MiddlewareConfig | None = None,
    ) -> ProxyMiddleware:

        return ProxyMiddleware(
            provider=resolver.resolve(
                ProxyProvider,
            ),
            policy=resolver.resolve(
                ProxyPolicy,
            ),
            config=config,
        )

    return factory
def build_retry_middleware_factory(
    resolver: Resolver[Any, Any],
) -> MiddlewareFactory:

    def factory(
        config: MiddlewareConfig | None = None,
    ) -> RetryMiddleware:

        return RetryMiddleware(
            policy=resolver.resolve(
                RetryPolicy,
            ),
            config=config,
        )

    return factory
def build_session_middleware_factory(
    resolver: Resolver[Any, Any],
) -> MiddlewareFactory:

    def factory(
        config: MiddlewareConfig | None = None,
    ) -> SessionMiddleware:

        return SessionMiddleware(
            store=resolver.resolve(
                SessionStore,
            ),
            policy=resolver.resolve(
                SessionPolicy,
            ),
            config=config,
        )

    return factory
def build_throttle_middleware_factory(
    resolver: Resolver[Any, Any],
) -> MiddlewareFactory:

    def factory(
        config: MiddlewareConfig | None = None,
    ) -> ThrottleMiddleware:

        return ThrottleMiddleware(
            limiter=resolver.resolve(
                ThrottleLimiter,
            ),
            resolver=resolver.resolve(
                ThrottleKeyResolver,
            ),
            policy=resolver.resolve(
                ThrottlePolicy,
            ),
            config=config,
        )

    return factory

class ApplicationContainerFactory:
    """
    Composition root of the application.

    Builds the complete application dependency graph
    using the frozen core Provider system.
    """

    def create(
        self,
        config: ApplicationConfig,
    ) -> ApplicationContainer:

        builder = ProviderBuilder(
            strategy_cls=SingletonProvider,
        )

        self._register_application_services(
            builder,
            config,
        )

        providers = builder.build()

        return ApplicationContainer(
            providers,
        )

    def _register_application_services(
        self,
        builder: ProviderBuilder,
        config: ApplicationConfig,
    ) -> None:
        
        self._register_lifecycle(
            builder,
        )

        self._register_spiders(
            builder,
            config,
        )

        self._register_adapters(
            builder,
        )

        self._register_runtimes(
            builder,
            config,
        )

        self._register_downloaders(
            builder,
        )

        self._register_middleware_dependencies(
            builder,
        )

        self._register_middlewares(
            builder,
        )

        self._register_events(
            builder,
        )

        self._register_request_services(
            builder,
        )

        self._register_extraction_services(
            builder,
        )

        self._register_spider_services(
            builder,
        )

        self._register_crawler(
            builder,
        )

    def _register_spiders(
        self,
        builder: ProviderBuilder,
        config: ApplicationConfig,
    ) -> None:

        registry = SpiderRegistry()

        for definition in config.spiders:
            registry.register(
                definition.name,
                definition.spider_type,
            )

        builder.add_instance(
            SpiderRegistry,
            registry,
        )

        builder.add_factory(
            SpiderFactory,
            lambda resolver: SpiderFactory(
                resolver,
            ),
        )

    def _register_adapters(
        self,
        builder: ProviderBuilder,
    ) -> None:

        builder.add_type(
            ResponseAdapterFactory,
        )

    def _register_runtimes(
        self,
        builder: ProviderBuilder,
        config: ApplicationConfig,
    ) -> None:

        builder.add_factory(
            AsyncCrawlerRunner,
            lambda _: ScrapyAsyncCrawlerRunner(),
        )

        builder.add_factory(
            ScrapyRuntime,
            lambda resolver: DefaultScrapyRuntime(
                runner=resolver.resolve(
                    AsyncCrawlerRunner,
                ),
                concurrency=config.runtime.concurrency,
                timeout=config.runtime.timeout,
            ),
        )

        builder.add_factory(
            ScrapyRequestExecutor,
            lambda resolver: DefaultScrapyRequestExecutor(
                runtime=resolver.resolve(
                    ScrapyRuntime,
                ),
            ),
        )

        builder.add_type(
            ScrapyRequestBridge,
        )

    def _register_downloaders(
        self,
        builder: ProviderBuilder,
    ) -> None:

        builder.add_factory(
            DownloaderRegistry,
            lambda resolver: self._create_downloader_registry(
                resolver,
            ),
        )

        builder.add_factory(
            DownloaderManager,
            lambda resolver: DownloaderManager(
                registry=resolver.resolve(
                    DownloaderRegistry,
                ),
                lifecycle=resolver.resolve(
                    LifecycleManager,
                ),
            ),
        )

    def _create_downloader_registry(
        self,
        resolver: Resolver[Any, Any],
    ) -> DownloaderRegistry:

        registry = DownloaderRegistry()

        registry.register(
            DownloaderType.HTTPX,
            create_httpx_downloader,
        )

        registry.register(
            DownloaderType.SCRAPY,
            build_scrapy_downloader_factory(resolver),
        )

        registry.register(
            DownloaderType.PLAYWRIGHT,
            create_playwright_downloader,
        )

        return registry

    def _register_middleware_dependencies(
        self,
        builder: ProviderBuilder,
    ) -> None:

        builder.add_type(
            AuthProvider,
            BasicAuthProvider,
        )

        builder.add_type(
            AuthPolicy,
        )

        builder.add_type(
            Cache,
            MemoryCache,
        )

        builder.add_type(
            CachePolicy,
        )

        builder.add_type(
            CacheKeyProvider,
            FingerprintCacheKeyProvider,
        )

        builder.add_type(
            CookiePolicy,
        )

        builder.add_type(
            DeduplicatePolicy,
        )

        builder.add_type(
            FingerprintProvider,
            DefaultFingerprintProvider,

        )

        builder.add_type(
            ProxyProvider,
        )

        builder.add_type(
            ProxyPolicy,
        )

        builder.add_type(
            RetryPolicy,
        )

        builder.add_type(
            SessionStore,
            MemorySessionStore,
        )

        builder.add_type(
            SessionPolicy,
        )

        builder.add_type(
            ThrottleLimiter,
            InMemoryThrottleLimiter,
        )

        builder.add_type(
            ThrottleKeyResolver,
            HostThrottleKeyResolver,
        )

        builder.add_type(
            ThrottlePolicy,
        )

    def _register_middlewares(
        self,
        builder: ProviderBuilder,
    ) -> None:

        builder.add_factory(
            MiddlewareRegistry,
            lambda resolver: self._create_middleware_registry(
                resolver,
            ),
        )

        builder.add_factory(
            MiddlewareManager,
            lambda resolver: MiddlewareManager(
                registry=resolver.resolve(
                    MiddlewareRegistry,
                ),
                lifecycle=resolver.resolve(
                    LifecycleManager,
                ),
            ),
        )

    def _create_middleware_registry(
        self,
        resolver: Resolver[Any, Any],
    ) -> MiddlewareRegistry:

        registry = MiddlewareRegistry()

        registry.register(
            MiddlewareType.AUTH,
            build_auth_middleware_factory(
                resolver,
            ),
        )
        registry.register(
            MiddlewareType.CACHE,
            build_cache_middleware_factory(
                resolver,
            ),
        )
        registry.register(
            MiddlewareType.COOKIE,
            build_cookie_middleware_factory(
                resolver,
            ),
        )
        registry.register(
            MiddlewareType.DEDUPLICATE,
            build_deduplicate_middleware_factory(
                resolver,
            ),
        )

        registry.register(
            MiddlewareType.FINGERPRINT,
            build_fingerprint_middleware_factory(
                resolver,
            ),
        )
        registry.register(
            MiddlewareType.PROXY,
            build_proxy_middleware_factory(
                resolver,
            ),
        )
        registry.register(
            MiddlewareType.RETRY,
            build_retry_middleware_factory(
                resolver,
            ),
        )
        registry.register(
            MiddlewareType.SESSION,
            build_session_middleware_factory(
                resolver,
            ),
        )
        registry.register(
            MiddlewareType.THROTTLE,
            build_throttle_middleware_factory(
                resolver,
            ),
        )

        return registry

    def _register_request_services(
        self,
        builder: ProviderBuilder,
    ) -> None:

        builder.add_factory(
            DownloaderRequestExecutor,
            lambda resolver: DownloaderRequestExecutor(
                manager=resolver.resolve(
                    DownloaderManager,
                ),
            ),
        )

        builder.add_factory(
            RequestExecutor,
            lambda resolver: resolver.resolve(
                DownloaderRequestExecutor,
            ),
        )
        builder.add_factory(
            RequestRunner,
            lambda resolver: RequestRunner(
                executor=resolver.resolve(RequestExecutor),
                middleware=resolver.resolve(MiddlewareManager),
                dispatcher=resolver.resolve(EventDispatcher),
            ),
        )

    def _register_extraction_services(
        self,
        builder: ProviderBuilder,
    ) -> None:

        builder.add_type(
            ExtractEngine,
        )

        builder.add_type(
            DiscoveryEngine,
        )

        builder.add_type(
            ResponseAdapterFactory,
        )

    def _register_spider_services(
        self,
        builder: ProviderBuilder,
    ) -> None:

        builder.add_factory(
            SpiderServices,
            lambda resolver: SpiderServices(
                request_runner=resolver.resolve(RequestRunner),
                extract_engine=resolver.resolve(ExtractEngine),
                discovery_engine=resolver.resolve(DiscoveryEngine),
                fingerprint_provider=resolver.resolve(FingerprintProvider),
                response_adapter_factory=resolver.resolve(ResponseAdapterFactory),
            ),
        )

    def _register_lifecycle(
        self,
        builder: ProviderBuilder,
    ) -> None:

        builder.add_type(
            LifecycleManager,
        )

    def _register_crawler(
        self,
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
            CrawlerRunner,
            lambda resolver: CrawlerRunner(
                registry=resolver.resolve(
                    SpiderRegistry,
                ),
                factory=resolver.resolve(
                    SpiderFactory,
                ),
                executor=resolver.resolve(
                    SpiderExecutor,
                ),
            ),
        )

        builder.add_factory(
            CrawlerService,
            lambda resolver: CrawlerService(
                runner=resolver.resolve(
                    CrawlerRunner,
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
            ),
        )

    def _register_events(
        self,
        builder: ProviderBuilder,
    ) -> None:

        builder.add_type(
            EventRegistry,
        )

        builder.add_factory(
            EventDispatcher,
            lambda resolver: EventDispatcher(
                registry=resolver.resolve(
                    EventRegistry,
                ),
            ),
        )