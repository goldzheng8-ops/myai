from abc import ABC
from abc import abstractmethod
from typing import Generic
from typing import TypeVar

T = TypeVar("T")


class TemplateCache(
    Generic[T],
    ABC,
):

    @abstractmethod
    def get(
        self,
        key: str,
    ) -> T | None:
        ...

    @abstractmethod
    def put(
        self,
        key: str,
        value: T,
    ) -> None:
        ...

    @abstractmethod
    def clear(
        self,
    ) -> None:
        ...