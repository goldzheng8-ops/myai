from core.request.context import RequestContext



from .config import StaticProxyProviderConfig
from .config import ProxyConfig
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
    ) -> ProxyConfig | None:

        return self.config.proxy