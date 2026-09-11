from collections.abc import Sequence
from typing import Any

from core.request.middleware.auth.apikey import ApiKeyAuthProvider
from core.request.middleware.auth.basic import BasicAuthProvider
from core.request.middleware.auth.bearer import BearerAuthProvider
from core.request.middleware.auth.config import AuthProviderConfigUnion
from core.request.middleware.auth.cookie import CookieAuthProvider
from core.request.middleware.auth.oauth2 import OAuth2ClientCredentialsProvider
from core.request.middleware.auth.provider import BaseAuthProvider


class AuthProviderFactory:

    def create(
        self,
        config: AuthProviderConfigUnion,
    ) -> BaseAuthProvider[Any]:

        match config.type:

            case "basic":
                return BasicAuthProvider(
                    config,
                )

            case "api_key":
                return ApiKeyAuthProvider(
                    config,
                )

            case "bearer":
                return BearerAuthProvider(
                    config
                )

            case "cookie":
                return CookieAuthProvider(
                    config
                )

            case "oauth2_client_credentials":
                return (
                    OAuth2ClientCredentialsProvider(
                        config
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
    ) -> dict[str, BaseAuthProvider[Any]]:

        providers: dict[str, BaseAuthProvider[Any]] = {}

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