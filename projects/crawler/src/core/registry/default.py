from __future__ import annotations

from collections.abc import Callable, Mapping
from typing import Generic

from .base import Registry
from .typing import K, V


class DefaultRegistry(
    Registry[K, V],
    Generic[K, V],
):
    """
    Registry with lazy value creation.

    Missing values are created automatically by
    the provided factory.
    """

    def __init__(
        self,
        factory: Callable[[K], V],
        values: Mapping[K, V] | None = None,
    ) -> None:

        super().__init__(values)

        self._factory = factory

    def get(
        self,
        key: K,
    ) -> V:

        value = self.get_or_none(key)

        if value is not None:
            return value

        value = self._factory(key)

        self.register(
            key,
            value,
        )

        return value