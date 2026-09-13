from core.request.builder import RequestBuilder
from core.request.config import RequestConfig
from core.spider.executor import SpiderExecutor


from .config import SpiderConfigUnion
from .result import SpiderResult



class CrawlerRunner:

    def __init__(
        self,
        executor: SpiderExecutor,
    ) -> None:

        self._executor = executor

    @property
    def executor(
        self,
    ) -> SpiderExecutor:
        return self._executor

    async def run(
        self,
        config: SpiderConfigUnion,
        start_requests: tuple[RequestConfig, ...],       
    ) -> SpiderResult:

        descriptors = tuple(
            RequestBuilder.from_request(
                request,
                kind=config.kind,
                profile=config.profile,
                target_spider=config.name
            )
            for request in start_requests
        )
        return await self._executor.execute(
            descriptors,            
        )