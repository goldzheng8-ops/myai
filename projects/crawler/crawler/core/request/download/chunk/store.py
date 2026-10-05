from __future__ import annotations

from abc import ABC, abstractmethod

from .model import ChunkRange


class ChunkStore(ABC):

    @abstractmethod
    async def start(self) -> None:
        ...

    @abstractmethod
    async def write(
        self,
        key: str,
        chunk: ChunkRange,
        body: bytes,
    ) -> None:
        ...

    @abstractmethod
    async def read(
        self,
        key: str,
        chunk: ChunkRange,
    ) -> bytes:
        ...

    @abstractmethod
    async def exists(
        self,
        key: str,
        chunk: ChunkRange,
    ) -> bool:
        ...

    @abstractmethod
    async def delete(
        self,
        key: str,
    ) -> None:
        ...