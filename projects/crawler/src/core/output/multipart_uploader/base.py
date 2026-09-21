from abc import ABC, abstractmethod
import asyncio
from dataclasses import dataclass
from typing import Any

from core.output.model import BinaryStream
from core.output.multipart_uploader.protocol import S3ClientProtocol

@dataclass(frozen=True, slots=True)
class MultipartPart:
    number: int
    body: bytes

class MultipartUploader(ABC):

    @abstractmethod
    async def upload(
        self,
        *,
        client: S3ClientProtocol,
        bucket: str,
        key: str,
        upload_id: str,
        source: BinaryStream,
    ) -> list[dict[str, Any]]:
        ...

class BaseMultipartUploader(
    MultipartUploader,
    ABC,
):

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