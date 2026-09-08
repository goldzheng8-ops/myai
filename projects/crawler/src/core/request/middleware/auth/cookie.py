from collections.abc import Mapping
from core.request.context import RequestContext

from .provider import AuthCredentials, AuthProvider

class CookieAuthProvider(AuthProvider):

    def __init__(
        self,
        cookies: Mapping[str, str],
    ) -> None:
        self._cookies = dict(cookies)

    async def provide(
        self,
        context: RequestContext,
    ) -> AuthCredentials:
        return AuthCredentials(
            cookies=self._cookies,
        )