
from application.crawler.application import CrawlerApplication
from application.crawler.service import CrawlerService
from core.lifecycle.manager import LifecycleManager
from core.provider import ProviderBuilder
from core.spider.executor import SpiderExecutor
from core.spider.registry import SpiderRegistry
from core.spider.runner import CrawlerRunner
from core.spider.services import SpiderServices


def register_crawler(
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