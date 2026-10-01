import base64

from core.request.context import RequestContext
from core.request.middleware.auth.auth_provider.config import BasicAuthProviderConfig
from .base import AuthCredentials, BaseAuthProvider
class BasicAuthProvider(BaseAuthProvider[BasicAuthProviderConfig]):

    def __init__(
        self,
        config:BasicAuthProviderConfig,
    ) -> None:
        super().__init__(config)

    async def get(
        self,
        context: RequestContext,
    ) -> AuthCredentials:
        raw = (
            f"{self.config.username}:{self.config.password}"
            .encode()
        )

        encoded = base64.b64encode(raw).decode()

        return AuthCredentials(
            headers={
                "Authorization": f"Basic {encoded}",
            },
        )