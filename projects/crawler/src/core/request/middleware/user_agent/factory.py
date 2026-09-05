
from collections.abc import Sequence
from typing import Any

from core.request.middleware.user_agent.config import UserAgentProviderConfigUnion
from core.request.middleware.user_agent.fake import FakeUserAgentProvider
from core.request.middleware.user_agent.provider import UserAgentProvider, UserAgentProviderMap
from core.request.middleware.user_agent.random import RandomUserAgentProvider
from core.request.middleware.user_agent.round_robin import RoundRobinUserAgentProvider
from core.request.middleware.user_agent.static import StaticUserAgentProvider


class UserAgentProviderFactory:

    def create(
        self,
        config: UserAgentProviderConfigUnion,
    ) -> UserAgentProvider[Any]:

        match config.type:

            case "static":
                return StaticUserAgentProvider(
                    config,
                )

            case "random":
                return RandomUserAgentProvider(
                    config,
                )

            case "round_robin":
                return RoundRobinUserAgentProvider(
                    config,
                )

            case "fake":
                return FakeUserAgentProvider(
                    config,
                )

            case _:
                raise TypeError(
                    "Unsupported user-agent provider "
                    f"type: {config.type!r}",
                )

    def create_all(
        self,
        configs: Sequence[
            UserAgentProviderConfigUnion
        ],
    ) -> UserAgentProviderMap:

        providers: UserAgentProviderMap = {}

        for config in configs:

            if config.name in providers:
                raise ValueError(
                    "Duplicate user-agent provider "
                    f"name: {config.name!r}",
                )

            providers[config.name] = self.create(
                config,
            )

        return providers