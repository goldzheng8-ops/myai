from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ProxyConfig:
    """
    Proxy configuration used by a request.
    """

    url: str

    username: str | None = None

    password: str | None = None