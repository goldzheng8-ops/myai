from application.config.model import CrawlRequest
from application.config.registry import SpiderConfigRegistry
from application.config.resolver import SpiderConfigResolver

from core.spider.result import CrawlResult
from core.spider.runner import CrawlerRunner


class CrawlerService:

    def __init__(
        self,
        runner: CrawlerRunner,
        registry: SpiderConfigRegistry,
        resolver: SpiderConfigResolver,
    ) -> None:

        self._runner = runner
        self._registry = registry
        self._resolver = resolver

    async def run(
        self,
        request: CrawlRequest,
    ) -> CrawlResult:

        base_config = self._registry.get(
            request.spider,
        )

        config = self._resolver.resolve(
            base_config,
            request.override,
        )
        if request.start_requests is None:
            return CrawlResult()
        return await self._runner.run(
            config,
            request.start_requests,
        )