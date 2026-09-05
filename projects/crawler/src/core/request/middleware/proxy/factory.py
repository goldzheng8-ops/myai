from __future__ import annotations
from typing import Any
from collections.abc import  Mapping, Sequence

from core.request.middleware.proxy.config import ProxyPoolProviderConfig, ProxyProviderConfigUnion
from core.request.middleware.proxy.country_proxy import CountryProxyProvider
from core.request.middleware.proxy.provider import ProxyProvider, ProxyProviderMap
from core.request.middleware.proxy.proxy_pool import ProxyPoolProvider
from core.request.middleware.proxy.random_proxy import RandomProxyProvider
from core.request.middleware.proxy.rotating_proxy import RotatingProxyProvider
from core.request.middleware.proxy.roundRobin_proxy import RoundRobinProxyProvider
from core.request.middleware.proxy.static_proxy import StaticProxyProvider

class ProxyProviderFactory:

    def create(
        self,
        config: ProxyProviderConfigUnion,
        *,
        providers: ProxyProviderMap | None = None,
    ) -> ProxyProvider[Any]:

        match config.type:

            case "static":
                return StaticProxyProvider(config)

            case "random":
                return RandomProxyProvider(config)

            case "round_robin":
                return RoundRobinProxyProvider(config)

            case "rotating":
                return RotatingProxyProvider(config)

            case "country":
                return CountryProxyProvider(config)

            case "pool":
                if providers is None:
                    raise RuntimeError(
                        "ProxyPoolProvider requires "
                        "ProxyProviderMap.",
                    )

                return ProxyPoolProvider(
                    config,
                    providers,
                )

            case _:
                raise TypeError(
                    "Unsupported proxy provider type: "
                    f"{config.type!r}",
                )

    def create_all(
        self,
        configs: Sequence[
            ProxyProviderConfigUnion
        ],
    ) -> ProxyProviderMap:

        providers: ProxyProviderMap = {}

        # First phase: normal providers.
        for config in configs:

            if config.type == "pool":
                continue

            if config.name in providers:
                raise ValueError(
                    f"Duplicate proxy provider name: "
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
                    f"Duplicate proxy provider name: "
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
        config: ProxyPoolProviderConfig,
        providers: Mapping[
            str,
            ProxyProvider[Any],
        ],
    ) -> None:

        for name in config.providers:

            if name not in providers:
                raise ValueError(
                    f"Proxy pool {config.name!r} "
                    f"references unknown provider "
                    f"{name!r}.",
                )