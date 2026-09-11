from collections.abc import Mapping
from typing import Any

from core.request.middleware.auth.provider import BaseAuthProvider


class AuthProviderResolver:

    def __init__(
        self,
        providers: Mapping[str, BaseAuthProvider[Any]],
    ) -> None:
        self._providers = dict(providers)

    def resolve(
        self,
        name: str,
    ) -> BaseAuthProvider[Any]:

        try:
            return self._providers[name]

        except KeyError as exc:
            raise LookupError(
                "Auth provider not found: "
                f"{name!r}",
            ) from exc

    def contains(
        self,
        name: str,
    ) -> bool:
        return name in self._providers

    def names(
        self,
    ) -> tuple[str, ...]:
        return tuple(self._providers)

    def values(
        self,
    ) -> tuple[BaseAuthProvider[Any], ...]:
        return tuple(self._providers.values())