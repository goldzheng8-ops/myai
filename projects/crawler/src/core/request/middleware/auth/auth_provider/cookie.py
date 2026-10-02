from core.request.context import RequestContext
from core.request.middleware.auth.auth_provider.config import CookieAuthProviderConfig
from core.request.middleware.auth.auth_state_provider import BrowserAuthStateProvider
from core.request.middleware.cookie.model import Cookie
from .base import AuthCredentials, BaseAuthProvider

class CookieAuthProvider(BaseAuthProvider[CookieAuthProviderConfig]):

    def __init__(
        self,
        auth_state_provider: BrowserAuthStateProvider,
        config: CookieAuthProviderConfig,
    ) -> None:
        super().__init__(config)
        self._auth_state_provider = auth_state_provider

    async def get(
        self,
        context: RequestContext,
    ) -> AuthCredentials | None:

        cookie = await self._get_cookie(
            context,
        )

        if cookie is None:
            return None

        return AuthCredentials(
            cookies=(cookie,),
        )

    async def _get_cookie(
        self,
        context: RequestContext,
    ) -> Cookie | None:

        state = await self._auth_state_provider.get_state(
            context=context,
        )

        for cookie in state.cookies:
            if cookie.name == self._config.name:
                return cookie

        return None