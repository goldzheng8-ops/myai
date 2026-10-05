from typing import Annotated, Literal


from pydantic import Field

from core.typing.config import BaseConfig

class AuthProviderConfig(BaseConfig):
    pass

class BasicAuthProviderConfig(
    AuthProviderConfig,
):
    type: Literal["basic"] = "basic"

    username: str

    password: str

class ApiKeyAuthProviderConfig(
    AuthProviderConfig,
):
    type: Literal["api_key"] = "api_key"

    key: str

    header: str = "X-API-Key"

class BearerAuthProviderConfig(
    AuthProviderConfig,
):
    type: Literal["bearer"] = "bearer"

    storage: Literal[
        "local_storage",
        "session_storage",
        "cookies",
    ]

    key: str

class CookieAuthProviderConfig(
    AuthProviderConfig,
):
    type: Literal["cookie"] = "cookie"

    name: str

class OAuth2CredentialsProviderConfig(
    AuthProviderConfig,
):
    type: Literal["oauth2"] = "oauth2"

    provider_key: str

    access_token_storage: Literal[
        "local_storage",
        "session_storage",
        "cookies",
    ]

    access_token_key: str

    refresh_token_storage: Literal[
        "local_storage",
        "session_storage",
        "cookies",
    ] | None = None

    refresh_token_key: str | None = None

    expires_at_storage: Literal[
        "local_storage",
        "session_storage",
        "cookies",
    ] | None = None

    expires_at_key: str | None = None

    token_type_storage: Literal[
        "local_storage",
        "session_storage",
        "cookies",
    ] | None = None

    token_type_key: str | None = None

    refresh_leeway: float = 30.0


AuthProviderConfigUnion = Annotated[
    (
        BasicAuthProviderConfig
        | ApiKeyAuthProviderConfig
        | BearerAuthProviderConfig
        | CookieAuthProviderConfig
        | OAuth2CredentialsProviderConfig
    ),
    Field(discriminator="type"),
]