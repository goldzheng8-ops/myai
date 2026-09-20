from abc import ABC, abstractmethod


class ResumeStore(ABC):

    @abstractmethod
    async def size(
        self,
        key: str,
    ) -> int:
        raise NotImplementedError

    @abstractmethod
    async def read(
        self,
        key: str,
    ) -> bytes:
        raise NotImplementedError

    @abstractmethod
    async def append(
        self,
        key: str,
        body: bytes,
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    async def delete(
        self,
        key: str,
    ) -> None:
        raise NotImplementedError

    async def start(self) -> None:
        pass

    async def close(self) -> None:
        pass