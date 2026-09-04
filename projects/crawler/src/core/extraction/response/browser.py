from __future__ import annotations

from abc import abstractmethod

from core.extraction.response.static import (
    StaticResponseAdapter,
)


class BrowserResponseAdapter(
    StaticResponseAdapter,
):
    """
    Response adapter for browser-based responses.

    Adds browser-specific capabilities while preserving
    the static response extraction API.
    """

    @abstractmethod
    async def scroll(
        self,
        *,
        count: int = 1,
        delay: float = 0.5,
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    async def close(
        self,
    ) -> None:
        raise NotImplementedError