
from application.config.model import CrawlRequest
from application.crawler.service import CrawlerService
from core.lifecycle.manager import LifecycleManager

from core.spider.result import SpiderResult

class CrawlerApplication:

    def __init__(
        self,
        service: CrawlerService,
        lifecycle: LifecycleManager,
    ) -> None:

        self._service = service
        self._lifecycle = lifecycle

    async def run(
        self,
        request: CrawlRequest,
    ) -> SpiderResult:

        return await self._service.run(
            request,
        )

    async def close(
        self,
    ) -> None:

        await self._lifecycle.close()