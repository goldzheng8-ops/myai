from core.request.context import RequestContext
from .provider import AuthCredentials, BaseAuthProvider

class ApiKeyAuthProvider(BaseAuthProvider):

    def __init__(
        self,
        key: str,
        header: str = "X-API-Key",
    ) -> None:
        self._key = key
        self._header = header

    async def get(
        self,
        context: RequestContext,
    ) -> AuthCredentials:
        return AuthCredentials(
            headers={
                self._header: self._key,
            },
        )