from __future__ import annotations

import asyncio
from typing import Any, AsyncIterator

from scrapy import Spider


class RuntimeSpider(Spider):
    """
    Internal long-lived spider used by the Scrapy runtime.

    This spider does not implement business crawling logic.
    It only keeps a Scrapy execution engine alive so that
    ExecutionEngine.download_async() can be used directly.
    """

    name = "ai_space_runtime"

    def __init__(
        self,
        *,
        stop_event: asyncio.Event,
        **kwargs: Any,
    ) -> None:

        super().__init__(
            **kwargs,
        )

        self._stop_event = stop_event

    async def start(self) -> AsyncIterator[None]:
        """
        Keep the spider alive until the runtime is closed.
        """

        await self._stop_event.wait()

        if False:
            yield