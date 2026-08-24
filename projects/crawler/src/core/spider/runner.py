from core.spider.executor import SpiderExecutor
from core.spider.factory import SpiderFactory

from .config import SpiderConfigUnion
from .context import SpiderContext
from .registry import SpiderRegistry
from .result import SpiderResult



class CrawlerRunner:

    def __init__(
        self,
        registry: SpiderRegistry,
        factory: SpiderFactory,
        executor: SpiderExecutor,
    ) -> None:

        self._registry = registry
        self._factory = factory
        self._executor = executor

    @property
    def registry(
        self,
    ) -> SpiderRegistry:
        return self._registry


    @property
    def factory(
        self,
    ) -> SpiderFactory:
        return self._factory


    @property
    def executor(
        self,
    ) -> SpiderExecutor:
        return self._executor

    async def run(
        self,
        config: SpiderConfigUnion,
    ) -> SpiderResult:

        spider_type = self._registry.get(
            config.template,
        )

        spider = self._factory.create(
            spider_type,
        )

        context = SpiderContext(
            config=config,
        )

        return await self._executor.execute(
            spider,
            context,
        )