from __future__ import annotations

from collections.abc import Awaitable, Callable, Sequence
from typing import Any, Final, Iterator

from ..context import RequestContext

from .base import RequestMiddleware
from .typing import RequestMiddlewareNext


RequestTerminal = Callable[
    [RequestContext],
    Awaitable[RequestContext],
]


def _wrap_handler(
    middleware: RequestMiddleware[Any],
    next_handler: RequestMiddlewareNext,
) -> RequestMiddlewareNext:
    async def handler(current: RequestContext) -> RequestContext:
        return await middleware.process(
            current,
            next_handler,
        )

    return handler


class MiddlewareChain:
    """
    Immutable request middleware execution chain.
    """

    __slots__ = (
        "_middlewares",
    )

    def __init__(
        self,
        middlewares: Sequence[RequestMiddleware[Any]],
    ) -> None:

        self._middlewares: Final[
            tuple[RequestMiddleware[Any], ...]
        ] = tuple(middlewares)

    @property
    def middlewares(
        self,
    ) -> tuple[RequestMiddleware[Any], ...]:

        return self._middlewares

    def __len__(
        self,
    ) -> int:

        return len(self._middlewares)

    def __iter__(self) -> Iterator[RequestMiddleware[Any]]:

        return iter(self._middlewares)

    async def execute(
        self,
        context: RequestContext,
        terminal: RequestTerminal,
    ) -> RequestContext:

        handler: RequestMiddlewareNext = terminal

        for middleware in reversed(
            self._middlewares
        ):
            handler = _wrap_handler(
                middleware,
                handler,
            )

        return await handler(context)