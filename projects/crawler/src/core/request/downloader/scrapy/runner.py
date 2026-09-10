from __future__ import annotations

import asyncio
from typing import Any, Protocol

from scrapy.crawler import (
    AsyncCrawlerRunner as ScrapyAsyncCrawlerRunner,
)
from scrapy.http import Request, Response
from scrapy.crawler import Crawler
from .spider import RuntimeSpider
from .settings import create_scrapy_settings

class AsyncCrawlerRunner(Protocol):
    """
    Application-level asynchronous bridge to Scrapy.
    """

    async def start(self) -> None:
        ...

    async def fetch(
        self,
        request: Request,
    ) -> Response:
        ...

    async def close(self) -> None:
        ...

class ScrapyAsyncCrawlerRunnerAdapter:

    def __init__(
        self,
        settings: dict[str, Any] | None = None,
    ) -> None:

        self._settings=create_scrapy_settings(settings)

        self._runner = ScrapyAsyncCrawlerRunner(
            self._settings,
        )

        self._crawler: Crawler | None = None

        self._crawl_task: asyncio.Task[None] | None = None

        self._ready = asyncio.Event()
        self._stop_event = asyncio.Event()

        self._started = False
        self._closed = False

    @property
    def runner(
        self,
    ) -> ScrapyAsyncCrawlerRunner:
        return self._runner

    @property
    def crawler(
        self,
    ) -> Crawler | None:
        return self._crawler

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
                "Cannot start a closed Scrapy runner.",
            )

        if self._started:
            return

        self._ready.clear()
        self._stop_event.clear()

        crawler = self._runner.create_crawler(
            RuntimeSpider,
        )

        self._crawler = crawler

        crawler.signals.connect(
            self._on_engine_started,
            signal="engine_started",
        )

        self._crawl_task = self._runner.crawl(
            crawler,
            stop_event=self._stop_event,
        )

        self._ready.set()

        try:
            await self._wait_until_ready()

        except BaseException:

            await self._cancel_crawl()

            self._crawler = None
            self._crawl_task = None

            raise

        self._started = True

    async def fetch(
        self,
        request: Request,
    ) -> Response:

        if self._closed:
            raise RuntimeError(
                "Scrapy runner is closed.",
            )

        if not self._started:
            await self.start()

        crawler = self._crawler

        if crawler is None:
            raise RuntimeError(
                "Scrapy crawler is unavailable.",
            )

        engine = crawler.engine

        return await engine.download_async(
            request,
        )

    async def close(self) -> None:

        if self._closed:
            return

        self._closed = True

        self._stop_event.set()

        try:
            await self._runner.stop()

        finally:

            task = self._crawl_task

            if task is not None:
                await asyncio.gather(
                    task,
                    return_exceptions=True,
                )

            self._crawl_task = None
            self._crawler = None
            self._started = False

    async def _wait_until_ready(
        self,
    ) -> None:

        task = self._crawl_task

        if task is None:
            raise RuntimeError(
                "Scrapy crawl task was not created.",
            )

        ready_task = asyncio.create_task(
            self._ready.wait(),
        )

        try:

            done, _ = await asyncio.wait(
                {
                    ready_task,
                    task,
                },
                return_when=asyncio.FIRST_COMPLETED,
            )

            if self._ready.is_set():
                return

            if task in done:

                if task.cancelled():
                    raise RuntimeError(
                        "Scrapy crawl task was cancelled "
                        "before the execution engine became ready.",
                    )

                exception = task.exception()

                if exception is not None:
                    raise exception

                raise RuntimeError(
                    "Scrapy runtime stopped before "
                    "the execution engine became ready.",
                )

        finally:

            if not ready_task.done():

                ready_task.cancel()

                await asyncio.gather(
                    ready_task,
                    return_exceptions=True,
                )

    async def _cancel_crawl(
        self,
    ) -> None:

        self._stop_event.set()

        try:
            await self._runner.stop()

        finally:

            task = self._crawl_task

            if task is not None:

                await asyncio.gather(
                    task,
                    return_exceptions=True,
                )

    def _on_engine_started(
        self,
        **_: Any,
    ) -> None:

        self._ready.set()