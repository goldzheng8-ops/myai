from core.request.context import RequestContext
from .provider import AuthCredentials, AuthProvider

class BearerAuthProvider(AuthProvider):

    def __init__(
        self,
        token: str,
    ) -> None:
        self._token = token

    async def provide(
        self,
        context: RequestContext,
    ) -> AuthCredentials:
        return AuthCredentials(
            headers={
                "Authorization":
                    f"Bearer {self._token}",
            },
        )