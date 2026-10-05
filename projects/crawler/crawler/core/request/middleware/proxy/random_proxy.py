import random

from core.request.context import RequestContext

from .config import RandomProxyProviderConfig
from .config import ProxyConfig
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
    ) -> ProxyConfig | None:

        if not self.config.proxies:
            return None

        return random.choice(
            self.config.proxies,
        )