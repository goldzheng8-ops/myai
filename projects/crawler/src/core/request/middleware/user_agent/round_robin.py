import asyncio
from core.request.context import RequestContext
from core.request.middleware.user_agent.config import RoundRobinUserAgentProviderConfig
from core.request.middleware.user_agent.provider import UserAgentProvider


class RoundRobinUserAgentProvider(
    UserAgentProvider[
        RoundRobinUserAgentProviderConfig
    ],
):
    def __init__(
        self,
        config: RoundRobinUserAgentProviderConfig,
    ) -> None:

        super().__init__(config)

        self._index = 0
        self._lock = asyncio.Lock()

    async def get(
        self,
        context: RequestContext,
    ) -> str | None:

        values = self.config.values

        if not values:
            return None

        async with self._lock:
            value = values[self._index]

            self._index = (
                self._index + 1
            ) % len(values)

        return value