from typing import Annotated, Literal

from pydantic import Field

from core.typing.config import BaseConfig

class AuthProviderConfig(BaseConfig):
    name: str

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

    token: str

class CookieAuthProviderConfig(
    AuthProviderConfig,
):
    type: Literal["cookie"] = "cookie"

    cookies: dict[str, str] = Field(
        default_factory=dict,
    )

class OAuth2ClientCredentialsProviderConfig(
    AuthProviderConfig,
):
    type: Literal[
        "oauth2_client_credentials"
    ] = "oauth2_client_credentials"

    token_url: str

    client_id: str

    client_secret: str

    scope: str | None = None

    timeout: float = 10.0

    token_expiry_margin: float = 30.0

AuthProviderConfigUnion = Annotated[
    (
        BasicAuthProviderConfig
        | ApiKeyAuthProviderConfig
        | BearerAuthProviderConfig
        | CookieAuthProviderConfig
        | OAuth2ClientCredentialsProviderConfig
    ),
    Field(discriminator="type"),
]