import asyncio
from typing import Any, Protocol, cast

import boto3
from botocore.client import BaseClient
from botocore.exceptions import ClientError

from core.output.config import S3StorageConfig
from core.output.model import BinaryStream
from core.output.storage.base import Storage
from core.output.stream.accumulator import StreamChunkAccumulator


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

    _MIN_MULTIPART_SIZE = 5 * 1024 * 1024
    _DEFAULT_PART_SIZE = 8 * 1024 * 1024

S3_MIN_MULTIPART_PART_SIZE = (
    5 * 1024 * 1024
)


class S3Storage(Storage):

    def __init__(
        self,
        config: S3StorageConfig,
    ) -> None:

        self._config = config

        if (
            config.multipart_part_size
            < S3_MIN_MULTIPART_PART_SIZE
        ):
            raise ValueError(
                "multipart_part_size must be at least "
                "5 MiB.",
            )

        self._client: S3ClientProtocol | None = None

        self._accumulator = (
            StreamChunkAccumulator(
                target_size=(
                    config.multipart_part_size
                ),
            )
        )

    @property
    def config(self) -> S3StorageConfig:
        return self._config

    async def start(self) -> None:
        if self._client is not None:
            return

        self._client = self._create_client()

    async def write_bytes(
        self,
        *,
        key: str,
        body: bytes,
        content_type: str | None = None,
        metadata: dict[str, str] | None = None,
        overwrite: bool = False,
    ) -> None:

        client = self._require_client()

        object_key = self._build_key(key)

        if not overwrite and await self.exists(key):
            raise FileExistsError(
                f"S3 object already exists: "
                f"s3://{self._config.bucket}/{object_key}",
            )

        kwargs: dict[str, Any] = {
            "Bucket": self._config.bucket,
            "Key": object_key,
            "Body": body,
        }
        if content_type is not None:
            kwargs["ContentType"] = content_type

        if metadata:
            kwargs["Metadata"] = metadata
        await asyncio.to_thread(
            client.put_object,
            **kwargs,
        )

    async def exists(
        self,
        key: str,
    ) -> bool:

        client = self._require_client()

        object_key = self._build_key(key)

        try:
            await asyncio.to_thread(
                client.head_object,
                Bucket=self._config.bucket,
                Key=object_key,
            )

        except ClientError as exc:

            if self._is_not_found(exc):
                return False

            raise

        return True

    async def close(self) -> None:
        self._client = None

    def _create_client(self) -> S3ClientProtocol:

        client: BaseClient = boto3.client(
            "s3",
            endpoint_url=self._config.endpoint_url,
            region_name=self._config.region,
            aws_access_key_id=self._config.access_key,
            aws_secret_access_key=self._config.secret_key,
        )

        return cast(
            S3ClientProtocol,
            client,
        )

    def _require_client(self) -> S3ClientProtocol:

        client = self._client

        if client is None:
            raise RuntimeError(
                "S3Storage is not started.",
            )

        return client

    def _build_key(
        self,
        key: str,
    ) -> str:

        key = key.lstrip("/")

        prefix = self._config.prefix.strip("/")

        if not prefix:
            return key

        return f"{prefix}/{key}"

    @staticmethod
    def _is_not_found(
        exc: ClientError,
    ) -> bool:

        response = exc.response

        if not isinstance(response, dict):
            return False

        error = response.get("Error")

        if not isinstance(error, dict):
            return False

        code = error.get("Code")

        return code in {
            "404",
            "NoSuchKey",
            "NotFound",
        }

    async def write_stream(
        self,
        *,
        key: str,
        body: BinaryStream,
        content_type: str | None = None,
        metadata: dict[str, str] | None = None,
        overwrite: bool = False,
    ) -> None:

        client = self._require_client()

        object_key = self._build_key(key)

        if (
            not overwrite
            and await self.exists(key)
        ):
            raise FileExistsError(
                f"S3 object already exists: "
                f"s3://{self._config.bucket}/{object_key}",
            )

        upload_id: str | None = None

        try:

            upload_id = (
                await self._create_multipart_upload(
                    client=client,
                    key=object_key,
                    content_type=content_type,
                    metadata=metadata,
                )
            )

            parts: list[dict[str, Any]] = []

            async for chunk in (
                self._accumulator.accumulate(body)
            ):

                part = await self._upload_part(
                    client=client,
                    key=object_key,
                    upload_id=upload_id,
                    part_number=len(parts) + 1,
                    body=chunk,
                )

                parts.append(part)

            if not parts:
                await self._abort_multipart_upload(
                    client=client,
                    key=object_key,
                    upload_id=upload_id,
                )

                upload_id = None

                await self.write_bytes(
                    key=key,
                    body=b"",
                    content_type=content_type,
                    metadata=metadata,
                    overwrite=overwrite,
                )

                return

            await self._complete_multipart_upload(
                client=client,
                key=object_key,
                upload_id=upload_id,
                parts=parts,
            )

            upload_id = None

        except BaseException:

            if upload_id is not None:

                try:
                    await self._abort_multipart_upload(
                        client=client,
                        key=object_key,
                        upload_id=upload_id,
                    )
                except Exception:
                    pass

            raise

    async def _create_multipart_upload(
        self,
        *,
        client: S3ClientProtocol,
        key: str,
        content_type: str | None,
        metadata: dict[str, str] | None,
    ) -> str:

        kwargs: dict[str, Any] = {
            "Bucket": self._config.bucket,
            "Key": key,
        }

        if content_type is not None:
            kwargs["ContentType"] = content_type

        if metadata:
            kwargs["Metadata"] = metadata

        response = await asyncio.to_thread(
            client.create_multipart_upload,
            **kwargs,
        )

        upload_id = response.get("UploadId")

        if not isinstance(upload_id, str):
            raise RuntimeError(
                "S3 create_multipart_upload response "
                "does not contain a valid UploadId.",
            )

        return upload_id

    async def _upload_part(
        self,
        *,
        client: S3ClientProtocol,
        key: str,
        upload_id: str,
        part_number: int,
        body: bytes,
    ) -> dict[str, Any]:

        response = await asyncio.to_thread(
            client.upload_part,
            Bucket=self._config.bucket,
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

    async def _complete_multipart_upload(
        self,
        *,
        client: S3ClientProtocol,
        key: str,
        upload_id: str,
        parts: list[dict[str, Any]],
    ) -> None:

        await asyncio.to_thread(
            client.complete_multipart_upload,
            Bucket=self._config.bucket,
            Key=key,
            UploadId=upload_id,
            MultipartUpload={
                "Parts": parts,
            },
        )

    async def _abort_multipart_upload(
        self,
        *,
        client: S3ClientProtocol,
        key: str,
        upload_id: str,
    ) -> None:

        await asyncio.to_thread(
            client.abort_multipart_upload,
            Bucket=self._config.bucket,
            Key=key,
            UploadId=upload_id,
        )