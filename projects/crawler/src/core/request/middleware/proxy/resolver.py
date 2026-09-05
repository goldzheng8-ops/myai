

from typing import Any, Mapping

from core.request.middleware.proxy.provider import ProxyProvider


class ProxyProviderResolver:

    def __init__(
        self,
        providers: Mapping[
            str,
            ProxyProvider[Any],
        ],
    ) -> None:
        self._providers = providers

    def resolve(
        self,
        name: str,
    ) -> ProxyProvider[Any]:

        try:
            return self._providers[name]
        except KeyError as exc:
            raise LookupError(
                f"Proxy provider not found: {name!r}",
            ) from exc