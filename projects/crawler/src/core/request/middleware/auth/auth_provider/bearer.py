from core.request.context import RequestContext
from core.request.middleware.auth.auth_provider.config import BearerAuthProviderConfig
from core.request.middleware.auth.auth_state_provider import BrowserAuthStateProvider

from .base import AuthCredentials, BaseAuthProvider

class BearerAuthProvider(BaseAuthProvider[BearerAuthProviderConfig]):

    def __init__(
        self,
        auth_state_provider: BrowserAuthStateProvider,
        config: BearerAuthProviderConfig,
    ) -> None:
        super().__init__(config)
        self._auth_state_provider = auth_state_provider


    async def get(
        self,
        context: RequestContext,
    ) -> AuthCredentials:

        token = await self._get_token(
            context,
        )

        if token is None:
            raise ValueError(
                f"Token with key '{self._config.key}' not found in the auth state.",
            )

        return AuthCredentials(
            headers={
                "Authorization": f"Bearer {token}",
            },
        )

    async def _get_token(
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
            return None
        raise ValueError(
            f"Unsupported browser storage: "
            f"{self._config.storage!r}",
        )