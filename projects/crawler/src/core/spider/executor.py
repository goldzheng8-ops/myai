from __future__ import annotations
import asyncio
from collections import deque
from typing import Sequence
import logging

from core.output.engine import OutputEngine
from core.request.descriptor import RequestDescriptor
from core.spider.dispatcher import RequestKindDispatcher
from core.spider.handler.base import RequestExecutionResult, ScheduledRequest

from .result import CrawlResult
from core.request.middleware.fingerprint.provider import FingerprintProvider

logger = logging.getLogger(__name__)

class CrawlerExecutor:

    def __init__(
        self,
        dispatcher: RequestKindDispatcher,
        fingerprint_provider: FingerprintProvider,
        output_engine: OutputEngine,
    ) -> None:
        self._dispatcher = dispatcher
        self._fingerprint_provider = (
            fingerprint_provider
        )
        self._output_engine = output_engine
    async def execute(
        self,
        descriptors: Sequence[RequestDescriptor],
    ) -> CrawlResult:

        result = CrawlResult()

        queue: deque[ScheduledRequest] = deque()
        seen: set[str] = set()

        for descriptor in descriptors:
            if self._enqueue(
                descriptor,
                queue,
                seen,
            ):
                result.request_count += 1

        while queue:

            item = queue.popleft()
            print(queue.__len__())
            try:
                execution = (
                    await self._dispatcher.execute(
                        item,
                    )
                )

            except asyncio.CancelledError:
                raise

            except Exception:
                logger.exception(
                    "Request failed: %s",
                    item.descriptor.url,
                )
                continue

            if execution.item is not None:

                await self._write_output(
                    execution,
                    result,
                )
            # if execution.download is not None:
            #     await self._output_engine.write_download(
            #         execution.download,
            #         execution.outputs,
            #     )

            for descriptor in execution.requests:

                if self._enqueue(
                    descriptor,
                    queue,
                    seen,
                ):
                    result.request_count += 1

            if not execution.continue_:
                break

        return result

    async def _write_output(
        self,
        execution: RequestExecutionResult,
        result: CrawlResult,
    ) -> None:

        if execution.item is None:
            return

        await self._output_engine.write(
            execution.item,
            execution.outputs,
        )

        result.item_count += 1

    def _enqueue(
        self,
        descriptor: RequestDescriptor,
        queue: deque[ScheduledRequest],
        seen: set[str],
    ) -> bool:

        fingerprint = (
            self._fingerprint_provider.fingerprint(
                descriptor,
            )
        )

        if not descriptor.meta.dont_filter:

            if fingerprint in seen:
                return False

            seen.add(fingerprint)

        queue.append(
            ScheduledRequest(
                descriptor=descriptor,
                fingerprint=fingerprint,
            ),
        )

        return True