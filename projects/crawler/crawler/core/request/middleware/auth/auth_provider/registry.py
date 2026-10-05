from typing import Any, Callable

from core.registry import Registry
from core.request.middleware.auth.auth_provider.base import BaseAuthProvider



AuthProviderFactory = Callable[
    [],
    BaseAuthProvider[Any],
]

class AuthProviderRegistry(
    Registry[
        str,
        AuthProviderFactory,
    ],
):
    """
    Registry of authentication provider factories.

    Each authentication configuration may optionally provide an
    authentication strategy.

    Absence of a registered provider means that the configuration
    does not require authentication.
    """

    def resolve(
        self,
        type_: str,
    ) -> BaseAuthProvider[Any]:

        factory = self.get(
            type_,
        )

        return factory()