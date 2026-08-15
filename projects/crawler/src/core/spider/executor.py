from collections import deque
from typing import Generic

from core.request.builder import RequestBuilder
from core.request.context import RequestContext
from core.request.descriptor import RequestDescriptor
from core.spider.typing import ConfigT


from .context import SpiderContext
from .result import SpiderResult
from .services import SpiderServices
from .template.base import TemplateSpider


class SpiderExecutor(Generic[ConfigT]):
    """
    Executes the request/discovery lifecycle of a spider.
    """

    def __init__(
        self,
        services: SpiderServices,
    ) -> None:

        self._services = services

    @property
    def services(self) -> SpiderServices:
        return self._services

    async def execute(
        self,
        spider: TemplateSpider[ConfigT],
        context: SpiderContext[ConfigT],
    ) -> SpiderResult:

        result = SpiderResult()

        queue: deque[RequestDescriptor] = deque()

        for request in context.config.start_requests:

            descriptor = RequestBuilder.from_request(
                request,
                kind=context.config.kind,
                profile=context.config.profile,
            )

            queue.append(
                descriptor,
            )

        seen: set[str] = set()

        while queue:

            descriptor = queue.popleft()

            request_context = RequestContext(
                descriptor=descriptor,
            )

            request_context = (
                await self._services.request_runner.run(
                    request_context,
                )
            )

            self._check_duplicate(
                request_context,
                seen,
            )

            step = await spider.process(
                context,
                request_context,
            )

            result.items.extend(
                step.items,
            )

            result.requests.extend(
                step.requests,
            )

            for descriptor in step.requests:
                queue.append(
                    descriptor,
                )

            if not step.continue_:
                break

        context.result = result

        return result