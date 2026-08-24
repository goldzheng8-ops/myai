
from application.crawler.service import CrawlerService
from core.lifecycle.manager import LifecycleManager
from core.spider.config import SpiderConfigUnion
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
        config: SpiderConfigUnion,
    ) -> SpiderResult:

        return await self._service.run(
            config,
        )

    async def close(
        self,
    ) -> None:

        await self._lifecycle.close()