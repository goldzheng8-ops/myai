from abc import ABC, abstractmethod
from typing import Generic, Iterable, Mapping, TypeVar

from core.plugin.base import Plugin


K = TypeVar("K")
V = TypeVar("V")
P = TypeVar("P", bound=Plugin)

class Registry(
    Generic[K, V],
):
    def __init__(

        self,

        values: Mapping[K, V] | None = None,

    ) -> None:

        self._values = dict(
            values or {}
        )

    def register(self,key: K,value: V,) -> None:
        if self.contains(key):

            raise ValueError(
                f"{key!r} already registered."
            )

        self._values[key] = value

    def contains(
        self,
        key: K,
    ) -> bool:

        return key in self._values

    def get(self,key:K) -> V:
        try:

            return self._values[key]

        except KeyError as exc:

            raise LookupError(
                f"{key!r} is not registered."
            ) from exc

    def remove(
        self,
        key: K,
    ) -> V:

        try:

            return self._values.pop(key)

        except KeyError as exc:

            raise LookupError(
                f"{key!r} is not registered."
            ) from exc

    def clear(
        self,
    ) -> None:

        self._values.clear()

    def keys(
        self,
    ):

        return self._values.keys()

    def values(
        self,
    ):

        return self._values.values()

    def items(
        self,
    ):

        return self._values.items()

    def __contains__(
        self,
        key: object,
    ) -> bool:

        return key in self._values

    def __len__(
        self,
    ) -> int:

        return len(
            self._values
        )

    def __iter__(
        self,
    ):

        return iter(
            self._values.items()
        )
class BasePluginRegistry(
    Registry[
        K,
        type[P],
    ],
    Generic[K, P],
    ABC,
):

    def __init__(
        self,
        plugins: Iterable[type[P]] = (),
    ) -> None:

        self._types: dict[K, type[P]] = {}

        for plugin in plugins:
            self.install(plugin)

    def install(
        self,
        plugin: type[P],
    ) -> None:
        self.register(
            self.resolve_key(plugin),
            plugin,
        )

    @staticmethod
    def resolve_key(
        plugin: type[P],
    ) -> K:
        return plugin.plugin_type

    @abstractmethod
    def create(
        self,
        key: K,
        *args: object,
        **kwargs: object,
    ) -> P:
        ...