import random

from core.request.context import RequestContext

from .config import RandomProxyProviderConfig
from .model import Proxy
from .provider import ProxyProvider


class RandomProxyProvider(
    ProxyProvider[RandomProxyProviderConfig],
):
    def __init__(
        self,
        config: RandomProxyProviderConfig,
    ) -> None:

        super().__init__(config)
    async def get(
        self,
        context: RequestContext,
    ) -> Proxy | None:

        if not self.config.proxies:
            return None

        proxy = random.choice(
            self.config.proxies,
        )

        return Proxy(
            url=proxy.as_url(),
        )