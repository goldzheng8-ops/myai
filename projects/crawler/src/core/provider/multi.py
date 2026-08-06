from __future__ import annotations

from abc import ABC
from typing import Any, Generic, ItemsView, KeysView

from core.registry.base import Registry
from core.typing.vars import K, T

from core.provider.protocol import Resolver


class MultiProvider(
    Generic[K, T],
    ABC,
):
    """
    Resolves multiple services from one key.

    Registry:

        K
            ↓
        tuple[type[T], ...]

    Result:

        K
            ↓
        tuple[T, ...]
    """

    def __init__(
        self,
        *,
        registry: Registry[
            K,
            tuple[type[T], ...],
        ],
        resolver: Resolver[Any,Any],
    ) -> None:

        self._registry = registry
        self._resolver = resolver

    @property
    def registry(
        self,
    ) -> Registry[
        K,
        tuple[type[T], ...],
    ]:

        return self._registry

    @property
    def resolver(
        self,
    ) -> Resolver[Any,Any]:

        return self._resolver

    # ---------------------------------------------------------

    def get(
        self,
        key: K,
    ) -> tuple[T, ...]:

        return tuple(
            self._resolver.resolve(service)
            for service in self._registry.get(key)
        )

    # ---------------------------------------------------------

    def contains(
        self,
        key: K,
    ) -> bool:

        return self._registry.contains(key)

    def keys(
        self,
    ) -> KeysView[K]:

        return self._registry.keys()

    def items(
        self,
    ) -> ItemsView[K, tuple[type[T], ...]]:

        return self._registry.items()

    def values(
        self,
    ) -> tuple[tuple[T, ...], ...]:

        return tuple(
            self.get(key)
            for key in self._registry.keys()
        )

    # ---------------------------------------------------------

    def __contains__(
        self,
        key: object,
    ) -> bool:

        return key in self._registry

    def __len__(
        self,
    ) -> int:

        return len(self._registry)