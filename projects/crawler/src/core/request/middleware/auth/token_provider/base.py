from abc import ABC, abstractmethod

from core.request.context import RequestContext


class TokenProvider(ABC):

    @abstractmethod
    async def get(
        self,
        context: RequestContext,
    ) -> str | None:
        """
        Return an authentication token for the current request.

        Returning None means that no token is currently available.
        """
        raise NotImplementedError