import asyncio
from collections.abc import AsyncIterable
from typing import Any

from core.output.multipart_uploader.base import MultipartUploader
from core.output.multipart_uploader.protocol import S3ClientProtocol
from core.output.stream.accumulator import StreamChunkAccumulator


class SerialMultipartUploader(
    MultipartUploader,
):

    def __init__(
        self,
        accumulator: StreamChunkAccumulator,
    ) -> None:
        self._accumulator = accumulator

    async def upload(
        self,
        *,
        client: S3ClientProtocol,
        bucket: str,
        key: str,
        upload_id: str,
        source: AsyncIterable[bytes],
    ) -> list[dict[str, Any]]:

        parts: list[dict[str, Any]] = []

        part_number = 1

        async for chunk in (
            self._accumulator.accumulate(source)
        ):

            part = await self._upload_part(
                client=client,
                bucket=bucket,
                key=key,
                upload_id=upload_id,
                part_number=part_number,
                body=chunk,
            )

            parts.append(part)

            part_number += 1

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