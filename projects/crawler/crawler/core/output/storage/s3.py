import asyncio
from typing import Any, cast

import boto3
from botocore.client import BaseClient
from botocore.exceptions import ClientError

from core.output.config import S3StorageConfig
from core.output.model import BinaryStream
from core.output.multipart_uploader.base import MultipartUploader
from core.output.multipart_uploader.parallel import ParallelMultipartUploader
from core.output.multipart_uploader.protocol import S3ClientProtocol
from core.output.multipart_uploader.serial import SerialMultipartUploader
from core.output.storage.base import Storage
from core.output.stream.accumulator import StreamChunkAccumulator




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

        self._multipart_uploader = (
            self._create_multipart_uploader()
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

        client = self._client

        if client is None:
            return

        self._client = None

        close = getattr(
            client,
            "close",
            None,
        )

        if close is not None:
            await asyncio.to_thread(close)

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

            upload_id = await self._create_multipart_upload(
                client=client,
                key=object_key,
                content_type=content_type,
                metadata=metadata,
            )

            parts = await self._multipart_uploader.upload(
                client=client,
                bucket=self._config.bucket,
                key=object_key,
                upload_id=upload_id,
                source=body,
            )

            if not parts:
                await self._safe_abort_multipart_upload(
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

            await self._safe_abort_multipart_upload(
                client=client,
                key=object_key,
                upload_id=upload_id,
            )

            raise

    async def _safe_abort_multipart_upload(
        self,
        *,
        client: S3ClientProtocol,
        key: str,
        upload_id: str | None,
    ) -> None:

        if upload_id is None:
            return

        try:
            await self._abort_multipart_upload(
                client=client,
                key=key,
                upload_id=upload_id,
            )
        except Exception:
            pass
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

    def _create_multipart_uploader(
        self,
    ) -> MultipartUploader:

        accumulator = StreamChunkAccumulator(
            target_size=self._config.multipart_part_size,
        )

        concurrency = (
            self._config.multipart_concurrency
        )

        if concurrency <= 1:
            return SerialMultipartUploader(
                accumulator,
            )

        return ParallelMultipartUploader(
            accumulator,
            concurrency=concurrency,
        )