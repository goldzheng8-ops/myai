from __future__ import annotations

from collections.abc import Awaitable, Callable, Sequence
from typing import Final, Iterator

from ..context import RequestContext

from .protocol import (
    RequestMiddleware,
    RequestMiddlewareNext,
)


RequestTerminal = Callable[
    [RequestContext],
    Awaitable[RequestContext],
]


class MiddlewareChain:
    """
    Immutable request middleware execution chain.
    """

    __slots__ = (
        "_middlewares",
    )

    def __init__(
        self,
        middlewares: Sequence[RequestMiddleware],
    ) -> None:

        self._middlewares: Final[
            tuple[RequestMiddleware, ...]
        ] = tuple(middlewares)

    @property
    def middlewares(
        self,
    ) -> tuple[RequestMiddleware, ...]:

        return self._middlewares

    def __len__(
        self,
    ) -> int:

        return len(self._middlewares)

    def __iter__(self) -> Iterator[RequestMiddleware]:

        return iter(self._middlewares)

    async def execute(
        self,
        context: RequestContext,
        terminal: RequestTerminal,
    ) -> RequestContext:

        handler = terminal

        for middleware in reversed(
            self._middlewares
        ):

            next_handler = handler

            async def handler(
                current: RequestContext,
                middleware: RequestMiddleware = middleware,
                next_handler: RequestMiddlewareNext = next_handler,
            ) -> RequestContext:

                return await middleware.process(
                    current,
                    next_handler,
                )

        return await handler(context)