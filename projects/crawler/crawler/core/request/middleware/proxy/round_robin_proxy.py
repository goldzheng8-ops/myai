import asyncio

from core.request.context import RequestContext


from .config import RoundRobinProxyProviderConfig
from .config import ProxyConfig
from .provider import ProxyProvider


class RoundRobinProxyProvider(
    ProxyProvider[RoundRobinProxyProviderConfig],
):

    def __init__(
        self,
        config: RoundRobinProxyProviderConfig,
    ) -> None:
        super().__init__(config)

        self._index = 0
        self._lock = asyncio.Lock()

    async def get(
        self,
        context: RequestContext,
    ) -> ProxyConfig | None:

        proxies = self.config.proxies

        if not proxies:
            return None

        async with self._lock:
            proxy = proxies[
                self._index % len(proxies)
            ]
            self._index += 1

        return proxy