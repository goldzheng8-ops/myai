import asyncio

from core.output.storage.base import Storage


from pathlib import Path


class LocalFileStorage(Storage):

    def __init__(
        self,
        directory: str,
    ) -> None:
        self._directory = Path(directory)

    async def start(self) -> None:
        await asyncio.to_thread(
            self._directory.mkdir,
            parents=True,
            exist_ok=True,
        )

    async def write_bytes(
        self,
        *,
        key: str,
        body: bytes,
        content_type: str | None = None,
        metadata: dict[str, str] | None = None,
        overwrite: bool = False,
    ) -> None:

        path = self._resolve_path(key)

        await asyncio.to_thread(
            path.parent.mkdir,
            parents=True,
            exist_ok=True,
        )

        if (
            path.exists()
            and not overwrite
        ):
            raise FileExistsError(
                f"File already exists: {path}",
            )

        await asyncio.to_thread(
            path.write_bytes,
            body,
        )

    async def exists(
        self,
        key: str,
    ) -> bool:

        path = self._resolve_path(key)

        return await asyncio.to_thread(
            path.exists,
        )

    async def close(self) -> None:
        return None

    def _resolve_path(
        self,
        key: str,
    ) -> Path:

        # 防止 key 脱离 storage 根目录
        path = (
            self._directory / key
        ).resolve()

        root = self._directory.resolve()

        if (
            path != root
            and root not in path.parents
        ):
            raise ValueError(
                f"Storage key escapes root directory: "
                f"{key!r}",
            )

        return path

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