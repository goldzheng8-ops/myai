from dataclasses import dataclass

from core.request.middleware.auth.token_provider.base import TokenProvider
from core.request.context import RequestContext


@dataclass(frozen=True, slots=True)
class StaticTokenProviderConfig:
    token: str


class StaticTokenProvider(
    TokenProvider,
):

    def __init__(
        self,
        config: StaticTokenProviderConfig,
    ) -> None:
        self._config = config

    async def get(
        self,
        context: RequestContext,
    ) -> str | None:

        return self._config.token