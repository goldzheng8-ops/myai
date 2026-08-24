from __future__ import annotations

import asyncio
from scrapy import Request
from .runner import AsyncCrawlerRunner 
from scrapy.http import Response
from typing import Protocol

class ScrapyRuntime(Protocol):
    async def start(self) -> None:
        ...

    async def execute(
        self,
        request: Request,
    ) -> Response:
        ...

    async def close(self) -> None:
        ...

class DefaultScrapyRuntime:
    """
    Default asyncio-based Scrapy runtime.

    Responsibilities:

    - manage Scrapy runtime lifecycle
    - limit request concurrency
    - enforce request timeout
    - track active requests
    - perform graceful shutdown

    Scrapy reactor and Deferred handling are delegated
    to AsyncCrawlerRunner.
    """

    def __init__(
        self,
        runner: AsyncCrawlerRunner,
        *,
        concurrency: int = 8,
        timeout: float | None = 30.0,
    ) -> None:

        if concurrency <= 0:
            raise ValueError(
                "concurrency must be greater than zero.",
            )

        if timeout is not None and timeout <= 0:
            raise ValueError(
                "timeout must be greater than zero.",
            )

        self._runner = runner

        self._concurrency=concurrency
        self._semaphore = asyncio.Semaphore(
            concurrency,
        )

        self._timeout = timeout

        self._started = False
        self._closed = False

        self._active_tasks: set[
            asyncio.Task[Response]
        ] = set()

    @property
    def runner(
        self,
    ) -> AsyncCrawlerRunner:
        return self._runner

    @property
    def concurrency(
        self,
    ) -> int:
        # Semaphore 没有公开 initial value，
        # 因此如果需要这个 property，
        # 最好单独保存 _concurrency。
        return self._concurrency

    @property
    def timeout(
        self,
    ) -> float | None:
        return self._timeout

    @property
    def started(
        self,
    ) -> bool:
        return self._started

    @property
    def closed(
        self,
    ) -> bool:
        return self._closed

    async def start(self) -> None:

        if self._closed:
            raise RuntimeError(
                "Cannot start a closed Scrapy runtime.",
            )

        if self._started:
            return

        await self._runner.start()

        self._started = True

    async def execute(
        self,
        request: Request,
    ) -> Response:

        if self._closed:
            raise RuntimeError(
                "Scrapy runtime is closed.",
            )

        await self.start()

        async with self._semaphore:

            task = asyncio.create_task(
                self._fetch(request),
            )

            self._active_tasks.add(task)

            try:
                return await task

            finally:
                self._active_tasks.discard(task)

    async def close(self) -> None:

        if self._closed:
            return

        self._closed = True

        tasks = tuple(self._active_tasks)

        if tasks:
            await asyncio.gather(
                *tasks,
                return_exceptions=True,
            )

        if self._started:
            await self._runner.close()

        self._started = False

    async def _fetch(
        self,
        request: Request,
    ) -> Response:

        fetch = self._runner.fetch(
            request,
        )

        if self._timeout is None:
            return await fetch

        return await asyncio.wait_for(
            fetch,
            timeout=self._timeout,
        )