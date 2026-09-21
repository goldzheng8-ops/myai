import asyncio
from collections.abc import AsyncIterable
from typing import Any

from core.output.multipart_uploader.base import MultipartUploader
from core.output.multipart_uploader.protocol import S3ClientProtocol
from core.output.stream.accumulator import StreamChunkAccumulator

class ParallelMultipartUploader(
    MultipartUploader,
):

    def __init__(
        self,
        accumulator: StreamChunkAccumulator,
        concurrency: int = 4,
    ) -> None:

        if concurrency <= 0:
            raise ValueError(
                "concurrency must be greater than zero.",
            )

        self._accumulator = accumulator
        self._concurrency = concurrency

    async def upload(
        self,
        *,
        client: S3ClientProtocol,
        bucket: str,
        key: str,
        upload_id: str,
        source: AsyncIterable[bytes],
    ) -> list[dict[str, Any]]:

        pending: set[
            asyncio.Task[dict[str, Any]]
        ] = set()

        parts: list[dict[str, Any]] = []

        part_number = 1

        try:

            async for chunk in (
                self._accumulator.accumulate(source)
            ):

                task = asyncio.create_task(
                    self._upload_part(
                        client=client,
                        bucket=bucket,
                        key=key,
                        upload_id=upload_id,
                        part_number=part_number,
                        body=chunk,
                    ),
                )

                pending.add(task)

                part_number += 1

                if len(pending) >= self._concurrency:

                    done, pending = await asyncio.wait(
                        pending,
                        return_when=(
                            asyncio.FIRST_COMPLETED
                        ),
                    )

                    for task in done:
                        parts.append(
                            task.result(),
                        )

            while pending:

                done, pending = await asyncio.wait(
                    pending,
                    return_when=(
                        asyncio.FIRST_COMPLETED
                    ),
                )

                for task in done:
                    parts.append(
                        task.result(),
                    )

        except BaseException:

            for task in pending:
                task.cancel()

            if pending:
                await asyncio.gather(
                    *pending,
                    return_exceptions=True,
                )

            raise

        parts.sort(
            key=lambda part: part["PartNumber"],
        )

        return parts

    @staticmethod
    async def _upload_part(
        *,
        client: S3ClientProtocol,
        bucket: str,
        key: str,
        upload_id: str,
        part_number: int,
        body: bytes,
    ) -> dict[str, Any]:

        response = await asyncio.to_thread(
            client.upload_part,
            Bucket=bucket,
            Key=key,
            UploadId=upload_id,
            PartNumber=part_number,
            Body=body,
        )

        etag = response.get("ETag")

        if not isinstance(etag, str):
            raise RuntimeError(
                "S3 upload_part response does not "
                "contain a valid ETag.",
            )

        return {
            "PartNumber": part_number,
            "ETag": etag,
        }