
from application.config.model import ApplicationConfig
from application.crawler.application import CrawlerApplication
from application.crawler.service import CrawlerService
from core.lifecycle.manager import LifecycleManager
from core.provider import ProviderBuilder
from core.spider.executor import SpiderExecutor
from core.spider.registry import SpiderRegistry
from core.spider.runner import CrawlerRunner
from core.spider.services import SpiderServices
from application.config.registry import SpiderConfigRegistry
from application.config.resolver import SpiderConfigResolver



def register_crawler(
    builder: ProviderBuilder,
    config: ApplicationConfig,
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
            default_spider=config.default_spider,
        ),
    )