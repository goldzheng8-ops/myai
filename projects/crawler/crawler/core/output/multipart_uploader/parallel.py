import asyncio
from typing import Any

from core.output.model import BinaryStream
from core.output.multipart_uploader.base import BaseMultipartUploader, MultipartPart
from core.output.multipart_uploader.protocol import S3ClientProtocol
from core.output.stream.accumulator import StreamChunkAccumulator

class ParallelMultipartUploader(
    BaseMultipartUploader,
):

    def __init__(
        self,
        accumulator: StreamChunkAccumulator,
        concurrency: int,
        queue_size: int | None = None,
    ) -> None:

        if concurrency <= 0:
            raise ValueError(
                "concurrency must be greater than zero.",
            )

        self._accumulator = accumulator
        self._concurrency = concurrency

        self._queue_size = (
            queue_size
            if queue_size is not None
            else concurrency * 2
        )

        if self._queue_size <= 0:
            raise ValueError(
                "queue_size must be greater than zero.",
            )

    async def upload(
        self,
        *,
        client: S3ClientProtocol,
        bucket: str,
        key: str,
        upload_id: str,
        source: BinaryStream,
    ) -> list[dict[str, Any]]:

        queue: asyncio.Queue[
            MultipartPart | None
        ] = asyncio.Queue(
            maxsize=self._queue_size,
        )

        async with asyncio.TaskGroup() as group:

            producer_task = group.create_task(
                self._produce(
                    source=source,
                    queue=queue,
                ),
            )

            consumer_tasks = [
                group.create_task(
                    self._consume(
                        client=client,
                        bucket=bucket,
                        key=key,
                        upload_id=upload_id,
                        queue=queue,
                    ),
                )
                for _ in range(self._concurrency)
            ]

        # producer_task.result() makes producer
        # exceptions explicit to the type checker.
        producer_task.result()

        parts: list[dict[str, Any]] = []

        for task in consumer_tasks:
            parts.extend(task.result())

        parts.sort(
            key=lambda part: part["PartNumber"],
        )

        return parts

    async def _produce(
        self,
        *,
        source: BinaryStream,
        queue: asyncio.Queue[
            MultipartPart | None
        ],
    ) -> None:

        part_number = 1

        async for chunk in self._accumulator.accumulate(
            source,
        ):

            await queue.put(
                MultipartPart(
                    number=part_number,
                    body=chunk,
                ),
            )

            part_number += 1

        for _ in range(self._concurrency):
            await queue.put(None)

    async def _consume(
        self,
        *,
        client: S3ClientProtocol,
        bucket: str,
        key: str,
        upload_id: str,
        queue: asyncio.Queue[
            MultipartPart | None
        ],
    ) -> list[dict[str, Any]]:

        parts: list[dict[str, Any]] = []

        while True:

            part = await queue.get()

            try:

                if part is None:
                    return parts

                result = await self._upload_part(
                    client=client,
                    bucket=bucket,
                    key=key,
                    upload_id=upload_id,
                    part_number=part.number,
                    body=part.body,
                )

                parts.append(result)

            finally:
                queue.task_done()