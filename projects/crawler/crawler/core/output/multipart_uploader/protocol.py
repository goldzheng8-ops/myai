
from typing import Any, Protocol


class S3ClientProtocol(Protocol):

    def put_object(
        self,
        *,
        Bucket: str,
        Key: str,
        Body: bytes,
        ContentType: str | None = None,
        Metadata: dict[str, str] | None = None,
    ) -> Any:
        ...

    def head_object(
        self,
        *,
        Bucket: str,
        Key: str,
    ) -> Any:
        ...

    def create_multipart_upload(
        self,
        *,
        Bucket: str,
        Key: str,
        ContentType: str | None = None,
        Metadata: dict[str, str] | None = None,
    ) -> Any:
        ...

    def upload_part(
        self,
        *,
        Bucket: str,
        Key: str,
        UploadId: str,
        PartNumber: int,
        Body: bytes,
    ) -> Any:
        ...

    def complete_multipart_upload(
        self,
        *,
        Bucket: str,
        Key: str,
        UploadId: str,
        MultipartUpload: dict[str, Any],
    ) -> Any:
        ...

    def abort_multipart_upload(
        self,
        *,
        Bucket: str,
        Key: str,
        UploadId: str,
    ) -> Any:
        ...