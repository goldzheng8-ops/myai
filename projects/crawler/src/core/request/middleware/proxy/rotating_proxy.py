import asyncio
import time

from core.request.context import RequestContext

from .config import RotatingProxyProviderConfig
from .model import Proxy
from .provider import ProxyProvider


class RotatingProxyProvider(
    ProxyProvider[RotatingProxyProviderConfig],
):

    def __init__(
        self,
        config: RotatingProxyProviderConfig,
    ) -> None:

        super().__init__(config)

        self._index = 0
        self._rotated_at = 0.0
        self._lock = asyncio.Lock()

    async def get(
        self,
        context: RequestContext,
    ) -> Proxy | None:

        proxies = self.config.proxies

        if not proxies:
            return None

        async with self._lock:
            now = time.monotonic()

            if (
                now - self._rotated_at
                >= self.config.interval
            ):
                self._index = (
                    self._index + 1
                ) % len(proxies)

                self._rotated_at = now

            proxy = proxies[self._index]

        return Proxy(
            url=proxy.as_url(),
        )