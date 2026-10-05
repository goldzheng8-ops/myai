from typing import Annotated, Literal
from dataclasses import dataclass
from pydantic import Field
from urllib.parse import quote, urlsplit, urlunsplit

from core.typing.config import BaseConfig

@dataclass(frozen=True, slots=True)
class ProxyConfig:
    """
    Proxy configuration used by a request.
    """

    url: str

    username: str | None = None

    password: str | None = None

    country: str | None = None

    def as_url(self) -> str:
        """
        Return the proxy URL with optional authentication.
        """

        if self.username is None:
            return self.url

        parts = urlsplit(self.url)

        username = quote(
            self.username,
            safe="",
        )

        password = (
            quote(
                self.password,
                safe="",
            )
            if self.password is not None
            else ""
        )

        host = parts.hostname or ""

        if parts.port is not None:
            host = f"{host}:{parts.port}"

        netloc = f"{username}:{password}@{host}"

        return urlunsplit(
            (
                parts.scheme,
                netloc,
                parts.path,
                parts.query,
                parts.fragment,
            )
        )

class ProxyProviderConfig(BaseConfig):
    """
    Base configuration for a proxy provider.
    """

    name: str


class StaticProxyProviderConfig(
    ProxyProviderConfig,
):
    type: Literal["static"] = "static"

    proxy: ProxyConfig


class RandomProxyProviderConfig(
    ProxyProviderConfig,
):
    type: Literal["random"] = "random"

    proxies: tuple[ProxyConfig, ...] = ()


class RoundRobinProxyProviderConfig(
    ProxyProviderConfig,
):
    type: Literal["round_robin"] = "round_robin"

    proxies: tuple[ProxyConfig, ...] = ()


class RotatingProxyProviderConfig(
    ProxyProviderConfig,
):
    type: Literal["rotating"] = "rotating"

    proxies: tuple[ProxyConfig, ...] = ()

    interval: float = 60.0


class CountryProxyProviderConfig(
    ProxyProviderConfig,
):
    type: Literal["country"] = "country"

    country: str

    proxies: tuple[ProxyConfig, ...] = ()


class ProxyPoolProviderConfig(
    ProxyProviderConfig,
):
    type: Literal["pool"] = "pool"

    providers: tuple[str, ...] = ()

    strategy: Literal[
        "random",
        "round_robin",
    ] = "round_robin"


ProxyProviderConfigUnion = Annotated[
    (
        StaticProxyProviderConfig
        | RandomProxyProviderConfig
        | RoundRobinProxyProviderConfig
        | RotatingProxyProviderConfig
        | CountryProxyProviderConfig
        | ProxyPoolProviderConfig
    ),
    Field(discriminator="type"),
]