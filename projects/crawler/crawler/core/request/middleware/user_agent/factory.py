
from collections.abc import Mapping, Sequence
from typing import Any

from core.request.middleware.user_agent.config import PoolUserAgentProviderConfig, UserAgentProviderConfigUnion
from core.request.middleware.user_agent.fake import FakeUserAgentProvider
from core.request.middleware.user_agent.pool import PoolUserAgentProvider
from core.request.middleware.user_agent.provider import UserAgentProvider, UserAgentProviderMap
from core.request.middleware.user_agent.random import RandomUserAgentProvider
from core.request.middleware.user_agent.round_robin import RoundRobinUserAgentProvider
from core.request.middleware.user_agent.static import StaticUserAgentProvider


class UserAgentProviderFactory:

    def create(
        self,
        config: UserAgentProviderConfigUnion,
        *,
        providers: UserAgentProviderMap | None = None,
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

            case "pool":
                if providers is None:
                    raise RuntimeError(
                        "PoolUserAgentProvider "
                        "requires UserAgentProviderMap.",
                    )

                return PoolUserAgentProvider(
                    config,
                    providers,
                )

            case _:
                raise TypeError(
                    "Unsupported user-agent provider type: "
                    f"{config.type!r}",
                )

    def create_all(
        self,
        configs: Sequence[
            UserAgentProviderConfigUnion
        ],
    ) -> UserAgentProviderMap:

        providers: UserAgentProviderMap = {}

        # First phase: normal providers.
        for config in configs:

            if config.type == "pool":
                continue

            if config.name in providers:
                raise ValueError(
                    f"Duplicate User-Agent provider name: "
                    f"{config.name!r}",
                )

            providers[config.name] = self.create(
                config,
            )

        # Second phase: pool providers.
        for config in configs:

            if config.type != "pool":
                continue

            if config.name in providers:
                raise ValueError(
                    f"Duplicate User-Agent provider name: "
                    f"{config.name!r}",
                )

            self._validate_pool(
                config,
                providers,
            )

            providers[config.name] = self.create(
                config,
                providers=providers,
            )

        return providers

    @staticmethod
    def _validate_pool(
        config: PoolUserAgentProviderConfig,
        providers: Mapping[
            str,
            UserAgentProvider[Any],
        ],
    ) -> None:

        for name in config.providers:

            if name not in providers:
                raise ValueError(
                    f"User-Agent pool {config.name!r} "
                    f"references unknown provider "
                    f"{name!r}.",
                )