
import asyncio

from core.request.context import RequestContext

from .config import CountryProxyProviderConfig
from .config import ProxyConfig
from .provider import ProxyProvider


class CountryProxyProvider(
    ProxyProvider[CountryProxyProviderConfig],
):

    def __init__(
        self,
        config: CountryProxyProviderConfig,
    ) -> None:
        super().__init__(config)
        self._index = 0
        self._lock = asyncio.Lock()

    async def get(
        self,
        context: RequestContext,
    ) -> ProxyConfig | None:

        proxies = tuple(
            proxy
            for proxy in self.config.proxies
            if (
                proxy.country is not None
                and proxy.country.upper()
                == self.config.country.upper()
            )
        )

        if not proxies:
            return None

        async with self._lock:
            proxy = proxies[
                self._index % len(proxies)
            ]
            self._index += 1

        return proxy