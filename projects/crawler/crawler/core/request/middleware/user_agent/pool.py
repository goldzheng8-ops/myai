import asyncio
import random
from typing import Any
from collections.abc import Mapping

from core.request.context import RequestContext
from core.request.middleware.user_agent.config import PoolUserAgentProviderConfig
from core.request.middleware.user_agent.provider import UserAgentProvider
class PoolUserAgentProvider(
    UserAgentProvider[
        PoolUserAgentProviderConfig
    ],
):

    def __init__(
        self,
        config: PoolUserAgentProviderConfig,
        providers: Mapping[
            str,
            UserAgentProvider[Any],
        ],
    ) -> None:
        super().__init__(config)

        self._providers = providers
        self._index = 0
        self._lock = asyncio.Lock()

    async def get(
        self,
        context: RequestContext,
    ) -> str | None:

        names = self.config.providers

        if not names:
            return None

        match self.config.strategy:

            case "random":
                name = random.choice(names)

            case "round_robin":
                async with self._lock:
                    name = names[
                        self._index % len(names)
                    ]
                    self._index += 1

            case _:
                raise ValueError(
                    "Unsupported User-Agent pool strategy: "
                    f"{self.config.strategy!r}",
                )

        try:
            provider = self._providers[name]
        except KeyError as exc:
            raise RuntimeError(
                f"User-Agent provider not found: "
                f"{name!r}",
            ) from exc

        return await provider.get(
            context,
        )