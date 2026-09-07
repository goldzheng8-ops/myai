from typing import Annotated, Literal

from core.typing.config import BaseConfig
from pydantic import Field


class UserAgentProviderConfig(BaseConfig):
    name: str


class StaticUserAgentProviderConfig(
    UserAgentProviderConfig,
):
    type: Literal["static"] = "static"
    user_agent: str


class RandomUserAgentProviderConfig(
    UserAgentProviderConfig,
):
    type: Literal["random"] = "random"
    user_agents: tuple[str, ...]


class RoundRobinUserAgentProviderConfig(
    UserAgentProviderConfig,
):
    type: Literal["round_robin"] = "round_robin"
    user_agents: tuple[str, ...]


class FakeUserAgentProviderConfig(
    UserAgentProviderConfig,
):
    type: Literal["fake"] = "fake"
    browsers: tuple[str, ...] = ()
    min_version: int | None = None
    max_version: int | None = None

class PoolUserAgentProviderConfig(UserAgentProviderConfig):
    type: Literal["pool"] = "pool"
    providers: tuple[str, ...]
    strategy: Literal[
        "random",
        "round_robin",
    ] = "random"


UserAgentProviderConfigUnion = Annotated[
    (
        StaticUserAgentProviderConfig
        | RandomUserAgentProviderConfig
        | RoundRobinUserAgentProviderConfig
        | FakeUserAgentProviderConfig
        | PoolUserAgentProviderConfig
    ),
    Field(discriminator="type"),
]

