from __future__ import annotations

from abc import ABC, abstractmethod

from .typing import RequestMiddlewareNext
from ..context import RequestContext





class RequestMiddleware(ABC):
    """
    Base class for request middleware.

    Middleware may execute logic before and/or after
    the next middleware in the chain.
    """

    name: str

    priority: int = 0

    enabled: bool = True

    @abstractmethod
    async def process(
        self,
        context: RequestContext,
        next_: RequestMiddlewareNext,
    ) -> RequestContext:
        """
        Process a request context.

        Implementations may perform work before calling
        next_, after calling next_, or both.
        """

        raise NotImplementedError