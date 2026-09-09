
from application.config.model import CrawlRequest
from application.crawler.service import CrawlerService
from core.lifecycle.manager import LifecycleManager

from core.spider.result import SpiderResult

class CrawlerApplication:

    def __init__(
        self,
        service: CrawlerService,
        lifecycle: LifecycleManager,
        default_spider: str,
    ) -> None:

        self._service = service
        self._lifecycle = lifecycle
        self._default_spider = default_spider

    async def start(self) -> None:
        await self._lifecycle.start()

    async def run(
        self,
        request: CrawlRequest | None = None,
    ) -> SpiderResult:
        await self.start()
        if request is None:
            request = CrawlRequest(
                spider=self._default_spider,
            )

        return await self._service.run(
            request,
        )

    async def close(
        self,
    ) -> None:

        await self._lifecycle.close()