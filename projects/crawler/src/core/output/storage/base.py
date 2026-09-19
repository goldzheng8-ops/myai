from abc import ABC, abstractmethod

class Storage(ABC):

    @abstractmethod
    async def start(self) -> None:
        raise NotImplementedError

    @abstractmethod
    async def write_bytes(
        self,
        *,
        key: str,
        body: bytes,
        content_type: str | None = None,
        metadata: dict[str, str] | None = None,
        overwrite: bool = True,
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    async def write_stream(
        self,
        *,
        key: str,
        body: bytes,
        content_type: str | None = None,
        metadata: dict[str, str] | None = None,
        overwrite: bool = True,
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    async def exists(
        self,
        key: str,
    ) -> bool:
        raise NotImplementedError

    @abstractmethod
    async def close(self) -> None:
        raise NotImplementedError