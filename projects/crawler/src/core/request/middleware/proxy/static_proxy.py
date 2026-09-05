from core.request.context import RequestContext



from .config import StaticProxyProviderConfig
from .model import Proxy
from .provider import ProxyProvider


class StaticProxyProvider(
    ProxyProvider[StaticProxyProviderConfig],
):
    def __init__(
        self,
        config: StaticProxyProviderConfig,
    ) -> None:

        super().__init__(config)
    async def get(
        self,
        context: RequestContext,
    ) -> Proxy:

        proxy = self.config.proxy

        return Proxy(
            url=proxy.as_url(),
        )