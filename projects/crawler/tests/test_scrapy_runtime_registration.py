import asyncio

from application.bootstrap.registration.runtimes import register_runtimes
from application.config.loader import YamlConfigLoader
from application.config.model import ApplicationConfig
from core.provider import ProviderBuilder
from core.request.downloader.scrapy.runner import (
    AsyncCrawlerRunner,
    ScrapyAsyncCrawlerRunnerAdapter,
)


def test_runtime_registration_uses_adapter_instance():
    builder = ProviderBuilder()
    config = YamlConfigLoader().load("application.yaml")

    register_runtimes(builder, config)

    instance = builder.build().resolve(AsyncCrawlerRunner)

    assert isinstance(instance, ScrapyAsyncCrawlerRunnerAdapter)


def test_scrapy_runner_start_does_not_hang():
    async def run_test() -> None:
        runner = ScrapyAsyncCrawlerRunnerAdapter()

        await asyncio.wait_for(runner.start(), timeout=5)

        assert runner.started is True

        await runner.close()

    asyncio.run(run_test())
