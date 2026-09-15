from core.spider.handler.base import RequestExecutionResult, ScheduledRequest
from core.spider.handler.registry import RequestKindHandlerRegistry


class RequestKindDispatcher:

    def __init__(
        self,
        registry: RequestKindHandlerRegistry,
    ) -> None:
        self._registry = registry

    async def execute(
        self,
        item: ScheduledRequest,
    ) -> RequestExecutionResult:

        handler = self._registry.get(
            item.descriptor.kind,
        )


        return await handler.execute(item)