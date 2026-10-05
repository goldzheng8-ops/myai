from __future__ import annotations
from collections.abc import Mapping
from typing import Generic, Protocol, Self
from collections.abc import (
    ItemsView,
    KeysView,
    ValuesView,
    Iterator,
)

from .typing import (
    K,
    V,
    V_co,
)


class ReadOnlyRegistryProtocol(
    Protocol,
    Generic[K, V_co],
):
    """
    Read-only registry protocol.
    """

    @property
    def frozen(self) -> bool:
        ...

    @property
    def is_empty(self) -> bool:
        ...

    def get(
        self,
        key: K,
    ) -> V_co:
        ...

    def require(
        self,
        key: K,
    ) -> V_co:
        ...

    def get_or_none(
        self,
        key: K,
    ) -> V_co | None:
        ...

    def contains(
        self,
        key: K,
    ) -> bool:
        ...

    def keys(
        self,
    ) -> KeysView[K]:
        ...

    def values(
        self,
    ) -> ValuesView[V_co]:
        ...

    def items(
        self,
    ) -> ItemsView[K, V_co]:
        ...

    def __contains__(
        self,
        key: object,
    ) -> bool:
        ...

    def __getitem__(
        self,
        key: K,
    ) -> V_co:
        ...

    def __len__(self) -> int:
        ...

    def __iter__(
        self,
    ) -> Iterator[tuple[K, V_co]]:
        ...



class MutableRegistryProtocol(
    ReadOnlyRegistryProtocol[K, V],
    Protocol,
    Generic[K, V],
):
    """
    Mutable registry protocol.
    """

    def freeze(self) -> Self:
        ...

    def register(
        self,
        key: K,
        value: V,
    ) -> None:
        ...

    def register_if_absent(
        self,
        key: K,
        value: V,
    ) -> V:
        ...

    def register_many(
        self,
        values: Mapping[K, V],
    ) -> None:
        ...

    def replace(
        self,
        key: K,
        value: V,
    ) -> None:
        ...

    def update(
        self,
        values: Mapping[K, V],
    ) -> None:
        ...

    def unregister(
        self,
        key: K,
    ) -> V:
        ...

    def clear(self) -> None:
        ...