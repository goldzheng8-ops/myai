from core.request.context import RequestContext
from core.request.middleware.auth.config import CookieAuthProviderConfig

from .provider import AuthCredentials, BaseAuthProvider

class CookieAuthProvider(BaseAuthProvider[CookieAuthProviderConfig]):

    def __init__(
        self,
        config: CookieAuthProviderConfig,
    ) -> None:
        super().__init__(config)

    async def get(
        self,
        context: RequestContext,
    ) -> AuthCredentials:
        return AuthCredentials(
            cookies=self.config.cookies,
        )