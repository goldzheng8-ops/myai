from dataclasses import dataclass

from core.request.context import RequestContext

from .provider import AuthCredentials, AuthProvider


@dataclass(slots=True)
class ApiKeyAuthProvider(AuthProvider):

    key: str

    header: str = "Authorization"

    prefix: str = "Bearer"

    async def provide(
        self,
        context: RequestContext,
    ) -> AuthCredentials:

        return AuthCredentials(
            headers={
                self.header:
                    f"{self.prefix} {self.key}",
            },
        )