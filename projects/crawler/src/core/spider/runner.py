from core.request.builder import RequestBuilder
from core.request.config import RequestConfig
from core.spider.executor import CrawlerExecutor


from .config import SpiderConfigUnion
from .result import CrawlResult



class CrawlerRunner:

    def __init__(
        self,
        executor: CrawlerExecutor,
    ) -> None:

        self._executor = executor

    @property
    def executor(
        self,
    ) -> CrawlerExecutor:
        return self._executor

    async def run(
        self,
        config: SpiderConfigUnion,
        start_requests: tuple[RequestConfig, ...],       
    ) -> CrawlResult:

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