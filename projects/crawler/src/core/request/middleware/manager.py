from __future__ import annotations

from collections.abc import Sequence

from .chain import MiddlewareChain
from .base import RequestMiddleware


class MiddlewareManager:
    """
    Manage request middleware definitions.

    Middleware are ordered by priority.
    Lower priority values execute first.
    """

    __slots__ = (
        "_middlewares",
    )

    def __init__(
        self,
        middlewares: Sequence[
            RequestMiddleware
        ] = (),
    ) -> None:

        self._middlewares: dict[
            str,
            RequestMiddleware,
        ] = {}

        for middleware in middlewares:
            self.register(middleware)

    # ---------------------------------------------------------
    # registration
    # ---------------------------------------------------------

    def register(
        self,
        middleware: RequestMiddleware,
    ) -> None:

        if middleware.name in self._middlewares:

            raise ValueError(
                f"Middleware "
                f"{middleware.name!r} "
                f"already registered."
            )

        self._middlewares[
            middleware.name
        ] = middleware

    def unregister(
        self,
        name: str,
    ) -> None:

        try:
            del self._middlewares[name]

        except KeyError as exc:

            raise LookupError(
                f"Middleware "
                f"{name!r} "
                f"is not registered."
            ) from exc

    # ---------------------------------------------------------
    # queries
    # ---------------------------------------------------------

    def get(
        self,
        name: str,
    ) -> RequestMiddleware:

        try:
            return self._middlewares[name]

        except KeyError as exc:

            raise LookupError(
                f"Middleware "
                f"{name!r} "
                f"is not registered."
            ) from exc

    def try_get(
        self,
        name: str,
    ) -> RequestMiddleware | None:

        return self._middlewares.get(name)

    def contains(
        self,
        name: str,
    ) -> bool:

        return name in self._middlewares

    def names(
        self,
    ) -> tuple[str, ...]:

        return tuple(
            self._middlewares,
        )

    def values(
        self,
    ) -> tuple[RequestMiddleware, ...]:

        return tuple(
            self._middlewares.values(),
        )

    def __len__(
        self,
    ) -> int:

        return len(self._middlewares)

    # ---------------------------------------------------------
    # ordering
    # ---------------------------------------------------------

    def ordered(
        self,
    ) -> tuple[RequestMiddleware, ...]:

        return tuple(
            sorted(
                (
                    middleware
                    for middleware
                    in self._middlewares.values()
                    if middleware.enabled
                ),
                key=lambda middleware: (
                    middleware.priority,
                    middleware.name,
                ),
            )
        )

    # ---------------------------------------------------------
    # chain
    # ---------------------------------------------------------

    def build_chain(
        self,
    ) -> MiddlewareChain:

        return MiddlewareChain(
            self.ordered(),
        )

    # ---------------------------------------------------------
    # mutation
    # ---------------------------------------------------------

    def clear(
        self,
    ) -> None:

        self._middlewares.clear()