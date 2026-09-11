from core.request.context import RequestContext
from core.request.middleware.auth.config import BearerAuthProviderConfig
from .provider import AuthCredentials, BaseAuthProvider

class BearerAuthProvider(BaseAuthProvider[BearerAuthProviderConfig]):

    def __init__(
        self,
        config: BearerAuthProviderConfig,
    ) -> None:
        super().__init__(config)

    async def get(
        self,
        context: RequestContext,
    ) -> AuthCredentials:
        return AuthCredentials(
            headers={
                "Authorization":
                    f"Bearer {self.config.token}",
            },
        )