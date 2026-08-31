from core.request.middleware.proxy.model import ProxyConfig
from core.request.context import RequestContext

class StaticProxyProvider:

    def __init__(
        self,
        proxy: ProxyConfig,
    ) -> None:
        self._proxy = proxy

    async def provide(
        self,
        context: RequestContext,
    ) -> ProxyConfig | None:

        return self._proxy