from abc import ABC, abstractmethod

from core.request.context import RequestContext


class RequestExecutor(ABC):
    """
    Executes a prepared request context.
    """

    @abstractmethod
    async def execute(
        self,
        context: RequestContext,
    ) -> RequestContext:
        raise NotImplementedError