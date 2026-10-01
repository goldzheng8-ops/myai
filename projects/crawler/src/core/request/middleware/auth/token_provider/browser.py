from core.request.middleware.auth.auth_state_provider import BrowserAuthStateProvider
from core.request.middleware.auth.token_provider.base import TokenProvider
from core.request.middleware.auth.token_provider.config import BrowserTokenProviderConfig
from core.request.context import RequestContext

class BrowserTokenProvider(TokenProvider):

    def __init__(
        self,
        auth_state_provider: BrowserAuthStateProvider,
        config: BrowserTokenProviderConfig,
    ) -> None:
        self._auth_state_provider = auth_state_provider
        self._config = config

    async def get(
        self,
        context: RequestContext,
    ) -> str | None:

        state = await self._auth_state_provider.get_state(
            context=context,
        )

        if self._config.storage == "local_storage":
            return state.local_storage.get(
                self._config.key,
            )

        if self._config.storage == "session_storage":
            return state.session_storage.get(
                self._config.key,
            )
        if self._config.storage == "cookies":
            for cookie in state.cookies:
                if cookie.name == self._config.key:
                    return cookie.value
        raise ValueError(
            f"Unsupported browser storage: "
            f"{self._config.storage!r}",
        )