from typing import Protocol

from core.request.context import RequestContext

from .model import ProxyConfig


class ProxyProvider(Protocol):

    async def provide(
        self,
        context: RequestContext,
    ) -> ProxyConfig | None:
        ...