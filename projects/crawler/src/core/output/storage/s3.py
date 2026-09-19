import asyncio
from typing import Any, Protocol, cast

import boto3
from botocore.client import BaseClient
from botocore.exceptions import ClientError

from core.output.config import S3StorageConfig
from core.output.storage.base import Storage


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


class S3Storage(Storage):

    def __init__(
        self,
        config: S3StorageConfig,
    ) -> None:
        self._config = config
        self._client: S3ClientProtocol | None = None

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
        body: bytes,
        content_type: str | None = None,
        metadata: dict[str, str] | None = None,
        overwrite: bool = True,
    ) -> None:
        pass