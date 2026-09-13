
from application.config.model import CrawlConfig, CrawlRequest
from application.crawler.service import CrawlerService
from core.lifecycle.manager import LifecycleManager

from core.spider.result import SpiderResult

class CrawlerApplication:

    def __init__(
        self,
        service: CrawlerService,
        lifecycle: LifecycleManager,
        crawl_config: CrawlConfig,
    ) -> None:
        self._service = service
        self._lifecycle = lifecycle
        self._crawl_config = crawl_config

    async def start(self) -> None:
        await self._lifecycle.start()

    async def run(
        self,
        request: CrawlRequest | None = None,
    ) -> SpiderResult:

        await self.start()

        request = self._crawl_config.create_request(
            request,
        )

        return await self._service.run(request)

    async def close(self) -> None:
        await self._lifecycle.close()