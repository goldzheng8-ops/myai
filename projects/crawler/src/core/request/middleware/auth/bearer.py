from core.request.context import RequestContext
from .provider import AuthCredentials, BaseAuthProvider

class BearerAuthProvider(BaseAuthProvider):

    def __init__(
        self,
        token: str,
    ) -> None:
        self._token = token

    async def get(
        self,
        context: RequestContext,
    ) -> AuthCredentials:
        return AuthCredentials(
            headers={
                "Authorization":
                    f"Bearer {self._token}",
            },
        )