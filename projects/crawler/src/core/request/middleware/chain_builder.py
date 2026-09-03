from typing import Any
from collections.abc import Sequence
from core.request.middleware.manager import MiddlewareManager
from core.request.middleware.base import RequestMiddleware
from core.request.middleware.chain import MiddlewareChain
from core.request.middleware.config import MiddlewareSpecUnion


class MiddlewareChainBuilder:

    def __init__(
        self,
        manager: MiddlewareManager,
    ) -> None:
        self._manager = manager

    async def build(
        self,
        specs: Sequence[MiddlewareSpecUnion],
    ) -> MiddlewareChain:

        entries: list[
            tuple[int, str, RequestMiddleware[Any]]
        ] = []

        for spec in specs:

            if not spec.enabled:
                continue

            middleware = await self._manager.get(
                spec,
            )

            entries.append(
                (
                    spec.priority,
                    middleware.name,
                    middleware,
                )
            )

        entries.sort(
            key=lambda item: (
                -item[0],
                item[1],
            )
        )

        return MiddlewareChain(
            tuple(
                item[2]
                for item in entries
            )
        )