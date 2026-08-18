

from typing import Any

from core.spider.executor import SpiderExecutor

from .config import SpiderConfigUnion
from .context import SpiderContext
from .registry import SpiderRegistry
from .result import SpiderResult



class CrawlerRunner:

    def __init__(
        self,
        registry: SpiderRegistry,
        executor: SpiderExecutor[Any],
    ) -> None:

        self._registry = registry
        self._executor = executor

    @property
    def registry(
        self,
    ) -> SpiderRegistry:

        return self._registry

    @property
    def executor(
        self,
    ) -> SpiderExecutor[Any]:

        return self._executor

    async def run(
        self,
        config: SpiderConfigUnion,
    ) -> SpiderResult:

        spider = self._registry.get(
            config.template,
        )

        context = SpiderContext(
            config=config,
        )

        return await self._executor.execute(
            spider,
            context,
        )