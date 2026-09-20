from __future__ import annotations

import asyncio
from pathlib import Path

from .model import ChunkRange
from .store import ChunkStore


class LocalChunkStore(ChunkStore):

    def __init__(
        self,
        directory: str | Path,
    ) -> None:
        self._directory = Path(directory)

    async def start(self) -> None:
        await asyncio.to_thread(
            self._directory.mkdir,
            parents=True,
            exist_ok=True,
        )

    async def write(
        self,
        key: str,
        chunk: ChunkRange,
        body: bytes,
    ) -> None:

        path = self._path(
            key,
            chunk,
        )

        path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        await asyncio.to_thread(
            path.write_bytes,
            body,
        )

    async def read(
        self,
        key: str,
        chunk: ChunkRange,
    ) -> bytes:

        path = self._path(
            key,
            chunk,
        )

        if not path.exists():
            return b""

        return await asyncio.to_thread(
            path.read_bytes,
        )

    async def exists(
        self,
        key: str,
        chunk: ChunkRange,
    ) -> bool:

        return await asyncio.to_thread(
            self._path(
                key,
                chunk,
            ).exists,
        )

    async def delete(
        self,
        key: str,
    ) -> None:

        directory = self._directory / key

        if not directory.exists():
            return

        await asyncio.to_thread(
            self._delete_directory,
            directory,
        )

    def _path(
        self,
        key: str,
        chunk: ChunkRange,
    ) -> Path:

        return (
            self._directory
            / key
            / f"{chunk.index:06d}.part"
        )

    @staticmethod
    def _delete_directory(
        directory: Path,
    ) -> None:

        for path in directory.iterdir():
            if path.is_file():
                path.unlink()

        directory.rmdir()