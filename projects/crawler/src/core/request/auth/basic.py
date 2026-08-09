import base64
from dataclasses import dataclass

from core.request.context import RequestContext

from .provider import AuthCredentials, AuthProvider


@dataclass(slots=True)
class BasicAuthProvider(AuthProvider):

    username: str

    password: str

    async def provide(
        self,
        context: RequestContext,
    ) -> AuthCredentials:

        raw = (
            f"{self.username}:{self.password}"
            .encode()
        )

        encoded = base64.b64encode(
            raw,
        ).decode()

        return AuthCredentials(
            headers={
                "Authorization":
                    f"Basic {encoded}",
            },
        )