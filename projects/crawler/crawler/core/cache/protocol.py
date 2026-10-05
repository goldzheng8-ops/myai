from __future__ import annotations

from abc import ABC, abstractmethod

from typing import Generic, TypeVar

K = TypeVar("K")
V = TypeVar("V")


class Cache(
    Generic[K, V],
    ABC,
):
    """
    Generic cache abstraction.

    A cache is a mutable key-value storage that may implement
    different eviction policies (LRU, TTL, LFU, etc.).
    """

    # ---------------------------------------------------------
    # Query
    # ---------------------------------------------------------

    @abstractmethod
    def contains(
        self,
        key: K,
    ) -> bool:
        ...

    @abstractmethod
    def get(
        self,
        key: K,
        default: V | None = None,
    ) -> V | None:
        ...

    @abstractmethod
    def get_or_raise(
        self,
        key: K,
    ) -> V:
        ...

    # ---------------------------------------------------------
    # Modify
    # ---------------------------------------------------------

    @abstractmethod
    def put(
        self,
        key: K,
        value: V,
    ) -> None:
        ...

    @abstractmethod
    def put_if_absent(
        self,
        key: K,
        value: V,
    ) -> bool:
        """
        Returns True if inserted.
        """
        ...

    @abstractmethod
    def update(
        self,
        values: dict[K, V],
    ) -> None:
        ...

    @abstractmethod
    def remove(
        self,
        key: K,
    ) -> bool:
        """
        Returns True if removed.
        """
        ...

    @abstractmethod
    def clear(
        self,
    ) -> None:
        ...

    # ---------------------------------------------------------
    # Views
    # ---------------------------------------------------------

    @abstractmethod
    def keys(
        self,
    ) -> tuple[K, ...]:
        ...

    # ---------------------------------------------------------
    # State
    # ---------------------------------------------------------

    @abstractmethod
    def size(
        self,
    ) -> int:
        ...

    @abstractmethod
    def is_empty(
        self,
    ) -> bool:
        ...

    # ---------------------------------------------------------
    # Magic
    # ---------------------------------------------------------

    def __contains__(
        self,
        key: object,
    ) -> bool:

        return self.contains(key)  # type: ignore[arg-type]

    def __len__(
        self,
    ) -> int:

        return self.size()