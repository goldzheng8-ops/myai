from typing import Annotated, Literal

from core.typing.config import BaseConfig
from pydantic import Field


class UserAgentProviderConfig(BaseConfig):
    name: str


class StaticUserAgentProviderConfig(
    UserAgentProviderConfig,
):
    type: Literal["static"] = "static"
    value: str


class RandomUserAgentProviderConfig(
    UserAgentProviderConfig,
):
    type: Literal["random"] = "random"
    values: tuple[str, ...]


class RoundRobinUserAgentProviderConfig(
    UserAgentProviderConfig,
):
    type: Literal["round_robin"] = "round_robin"
    values: tuple[str, ...]


class FakeUserAgentProviderConfig(
    UserAgentProviderConfig,
):
    type: Literal["fake"] = "fake"
    browsers: tuple[str, ...] = ()
    min_version: int | None = None
    max_version: int | None = None




UserAgentProviderConfigUnion = Annotated[
    (
        StaticUserAgentProviderConfig
        | RandomUserAgentProviderConfig
        | RoundRobinUserAgentProviderConfig
        | FakeUserAgentProviderConfig
    ),
    Field(discriminator="type"),
]