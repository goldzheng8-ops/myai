from core.request.context import RequestContext
from .provider import AuthCredentials, AuthProvider

class OAuth2ClientCredentialsProvider(AuthProvider):

    def __init__(
        self,
        token_url: str,
        client_id: str,
        client_secret: str,
        scope: str | None = None,
    ) -> None:
        self._token_url = token_url
        self._client_id = client_id
        self._client_secret = client_secret
        self._scope = scope

    async def provide(
        self,
        context: RequestContext,
    ) -> AuthCredentials:
        ...