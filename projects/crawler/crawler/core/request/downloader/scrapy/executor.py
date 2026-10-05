from __future__ import annotations
from typing import Protocol
from core.request.downloader.scrapy.runtime import ScrapyRuntime
from scrapy import Request
from scrapy.http import Response




class ScrapyRequestExecutor(Protocol):

    async def start(self) -> None:
        ...

    async def execute(
        self,
        request: Request,
    ) -> Response:
        ...

    async def close(self) -> None:
        ...

class DefaultScrapyRequestExecutor:
    def __init__(
        self,
        runtime: ScrapyRuntime,
    ) -> None:
        self._runtime = runtime

    async def start(self) -> None:
        await self._runtime.start()

    async def execute(
        self,
        request: Request,
    ) -> Response:
        return await self._runtime.execute(request)

    async def close(self) -> None:
        await self._runtime.close()