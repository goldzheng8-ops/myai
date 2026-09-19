import asyncio
from pathlib import Path

from core.download.resume.base import ResumeStore


class LocalResumeStore(
    ResumeStore,
):

    def __init__(
        self,
        directory: str | Path,
    ) -> None:

        self._directory = Path(directory)

    async def start(self) -> None:
        self._directory.mkdir(
            parents=True,
            exist_ok=True,
        )

    async def size(
        self,
        key: str,
    ) -> int:

        path = self._path(key)

        if not path.exists():
            return 0

        return path.stat().st_size

    async def read(
        self,
        key: str,
    ) -> bytes:

        path = self._path(key)

        if not path.exists():
            return b""

        return await asyncio.to_thread(
            path.read_bytes,
        )

    async def append(
        self,
        key: str,
        body: bytes,
    ) -> None:

        path = self._path(key)

        path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        def _append() -> None:
            with path.open("ab") as file:
                file.write(body)

        await asyncio.to_thread(
            _append,
        )

    async def delete(
        self,
        key: str,
    ) -> None:

        path = self._path(key)

        if not path.exists():
            return

        await asyncio.to_thread(
            path.unlink,
        )

    def _path(
        self,
        key: str,
    ) -> Path:

        return self._directory / (
            f"{key}.part"
        )