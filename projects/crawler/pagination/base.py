from abc import ABC

from adapters.base import ResponseAdapter
from config.config import PaginationConfig
from request.context import RequestContext


class PaginationPlugin(ABC):

    @property
    @abstractmethod
    def name(self) -> str:
        ...

    @abstractmethod
    async def paginate(
        self,
        response: ResponseAdapter,
        request: RequestContext,
        config: PaginationConfig,
    ) -> PaginationResult:
        ...