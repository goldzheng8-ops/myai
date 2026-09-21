from abc import ABC, abstractmethod
from typing import Any, AsyncIterable

from core.output.multipart_uploader.protocol import S3ClientProtocol


class MultipartUploader(ABC):

    @abstractmethod
    async def upload(
        self,
        *,
        client: S3ClientProtocol,
        bucket: str,
        key: str,
        upload_id: str,
        source: AsyncIterable[bytes],
    ) -> list[dict[str, Any]]:
        ...