from collections.abc import Mapping
from typing import Any

from core.request.middleware.auth.provider import AuthProvider


class AuthProviderResolver:

    def __init__(
        self,
        providers: Mapping[str, AuthProvider[Any]],
    ) -> None:
        self._providers = dict(providers)

    def resolve(
        self,
        name: str,
    ) -> AuthProvider[Any]:

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
    ) -> tuple[AuthProvider[Any], ...]:
        return tuple(self._providers.values())