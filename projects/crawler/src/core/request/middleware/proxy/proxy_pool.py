import asyncio
import random
from typing import Any
from collections.abc import Mapping

from core.request.context import RequestContext
from core.request.middleware.proxy.config import ProxyPoolProviderConfig
from core.request.middleware.proxy.model import Proxy
from core.request.middleware.proxy.provider import ProxyProvider


class ProxyPoolProvider(
    ProxyProvider[ProxyPoolProviderConfig],
):

    def __init__(
        self,
        config: ProxyPoolProviderConfig,
        providers: Mapping[
            str,
            ProxyProvider[Any],
        ],
    ) -> None:
        super().__init__(config)

        self._providers = providers
        self._index = 0
        self._lock = asyncio.Lock()

    async def get(
        self,
        context: RequestContext,
    ) -> Proxy | None:

        names = self.config.providers

        if not names:
            return None

        if self.config.strategy == "random":
            name = random.choice(names)

        else:
            async with self._lock:
                name = names[
                    self._index % len(names)
                ]
                self._index += 1

        try:
            provider = self._providers[name]
        except KeyError as exc:
            raise RuntimeError(
                f"Proxy provider not found: {name!r}",
            ) from exc

        return await provider.get(context)