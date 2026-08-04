from abc import ABC, abstractmethod
from typing import Generic
from .typing import K, V

class Cache(
    Generic[K, V],
    ABC,
):

    @abstractmethod
    def get(
        self,
        key: K,
    ) -> V | None:
        ...

    @abstractmethod
    def put(
        self,
        key: K,
        value: V,
    ) -> None:
        ...

    @abstractmethod
    def contains(
        self,
        key: K,
    ) -> bool:
        ...

    @abstractmethod
    def remove(
        self,
        key: K,
    ) -> None:
        ...

    @abstractmethod
    def clear(
        self,
    ) -> None:
        ...

    @abstractmethod
    def keys(
        self,
    ) -> tuple[K, ...]:
        ...

    @abstractmethod
    def size(
        self,
    ) -> int:
        ...