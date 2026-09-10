
from application.config.model import ApplicationConfig
from core.provider import ProviderBuilder
from core.request.downloader.scrapy.bridge import ScrapyRequestBridge
from core.request.downloader.scrapy.executor import DefaultScrapyRequestExecutor, ScrapyRequestExecutor
from core.request.downloader.scrapy.runner import (
    AsyncCrawlerRunner,
    ScrapyAsyncCrawlerRunnerAdapter,
)
from core.request.downloader.scrapy.runtime import DefaultScrapyRuntime, ScrapyRuntime


def register_runtimes(
    builder: ProviderBuilder,
    config: ApplicationConfig,
) -> None:

    builder.add_factory(
        AsyncCrawlerRunner,
        lambda _: ScrapyAsyncCrawlerRunnerAdapter(),
    )

    builder.add_factory(
        ScrapyRuntime,
        lambda resolver: DefaultScrapyRuntime(
            runner=resolver.resolve(
                AsyncCrawlerRunner,
            ),
            concurrency=config.runtime.engine.concurrency,
            timeout=config.runtime.engine.timeout,
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