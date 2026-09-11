from core.request.context import RequestContext
from core.request.middleware.auth.config import ApiKeyAuthProviderConfig
from .provider import AuthCredentials, BaseAuthProvider

class ApiKeyAuthProvider(BaseAuthProvider[ApiKeyAuthProviderConfig]):

    def __init__(
        self,
        config: ApiKeyAuthProviderConfig,

    ) -> None:
        super().__init__(config)

    async def get(
        self,
        context: RequestContext,
    ) -> AuthCredentials:
        return AuthCredentials(
            headers={
                self.config.header: self.config.key,
            },
        )