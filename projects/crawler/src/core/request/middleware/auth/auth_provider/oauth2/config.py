from core.typing.config import BaseConfig

class OAuth2TokenEndpointConfig(BaseConfig):
    token_url: str

    client_id: str | None = None
    client_secret: str | None = None

    client_auth_method: str = "client_secret_post"

    timeout: float = 30.0