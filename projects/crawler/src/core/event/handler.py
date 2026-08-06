from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Generic, TypeVar

E = TypeVar("E")


class EventHandler(
    ABC,
    Generic[E],
):
    event: type[E] | None = None
    priority: int = 0

    @abstractmethod
    async def handle(
        self,
        event: E,
    ) -> None:
        ...