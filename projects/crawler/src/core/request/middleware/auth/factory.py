from collections.abc import Sequence
from typing import Any

from core.request.middleware.auth.apikey import ApiKeyAuthProvider
from core.request.middleware.auth.basic import BasicAuthProvider
from core.request.middleware.auth.bearer import BearerAuthProvider
from core.request.middleware.auth.config import AuthProviderConfigUnion
from core.request.middleware.auth.cookie import CookieAuthProvider
from core.request.middleware.auth.oauth2 import OAuth2ClientCredentialsProvider
from core.request.middleware.auth.provider import AuthProvider


class AuthProviderFactory:

    def create(
        self,
        config: AuthProviderConfigUnion,
    ) -> AuthProvider[Any]:

        match config.type:

            case "basic":
                return BasicAuthProvider(
                    username=config.username,
                    password=config.password,
                )

            case "api_key":
                return ApiKeyAuthProvider(
                    key=config.key,
                    header=config.header,
                )

            case "bearer":
                return BearerAuthProvider(
                    token=config.token,
                )

            case "cookie":
                return CookieAuthProvider(
                    cookies=config.cookies,
                )

            case "oauth2_client_credentials":
                return (
                    OAuth2ClientCredentialsProvider(
                        token_url=config.token_url,
                        client_id=config.client_id,
                        client_secret=config.client_secret,
                        scope=config.scope,
                        timeout=config.timeout,
                        token_expiry_margin=(
                            config.token_expiry_margin
                        ),
                    )
                )

            case _:
                raise TypeError(
                    "Unsupported auth provider type: "
                    f"{config.type!r}",
                )

    def create_all(
        self,
        configs: Sequence[
            AuthProviderConfigUnion
        ],
    ) -> dict[str, AuthProvider[Any]]:

        providers: dict[str, AuthProvider[Any]] = {}

        for config in configs:

            if config.name in providers:
                raise ValueError(
                    "Duplicate auth provider name: "
                    f"{config.name!r}",
                )

            providers[config.name] = self.create(
                config,
            )

        return providers