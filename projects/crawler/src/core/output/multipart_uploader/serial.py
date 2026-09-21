from typing import Any

from core.output.model import BinaryStream
from core.output.multipart_uploader.base import BaseMultipartUploader
from core.output.multipart_uploader.protocol import S3ClientProtocol
from core.output.stream.accumulator import StreamChunkAccumulator


class SerialMultipartUploader(
    BaseMultipartUploader,
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
        source: BinaryStream,
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

