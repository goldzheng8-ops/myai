import base64

from core.request.context import RequestContext
from .provider import AuthCredentials, AuthProvider
class BasicAuthProvider(AuthProvider):

    def __init__(
        self,
        username: str,
        password: str,
    ) -> None:
        self._username = username
        self._password = password

    async def provide(
        self,
        context: RequestContext,
    ) -> AuthCredentials:
        raw = (
            f"{self._username}:{self._password}"
            .encode()
        )

        encoded = base64.b64encode(raw).decode()

        return AuthCredentials(
            headers={
                "Authorization": f"Basic {encoded}",
            },
        )