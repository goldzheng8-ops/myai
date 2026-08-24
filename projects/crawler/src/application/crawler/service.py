from core.spider.config import SpiderConfigUnion
from core.spider.result import SpiderResult
from core.spider.runner import CrawlerRunner


class CrawlerService:

    def __init__(
        self,
        runner: CrawlerRunner,
    ) -> None:
        self._runner = runner

    async def run(
        self,
        config: SpiderConfigUnion,
    ) -> SpiderResult:

        return await self._runner.run(
            config,
        )