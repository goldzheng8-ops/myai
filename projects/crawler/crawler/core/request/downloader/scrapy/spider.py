from __future__ import annotations

import asyncio
from typing import Any
from collections.abc import AsyncIterator
from scrapy import Spider


class RuntimeSpider(Spider):
    """
    Internal long-lived spider used by the Scrapy runtime.
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

    async def start(
        self,
    ) -> AsyncIterator[None]:

        while not self._stop_event.is_set():
            await asyncio.sleep(0.1)

        if False:
            yield