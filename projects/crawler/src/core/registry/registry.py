from __future__ import annotations
from collections.abc import (
    ItemsView,
    Iterator,
    KeysView,
    Mapping,
    ValuesView,
)
from typing import Generic, Self

from .protocol import MutableRegistryProtocol
from .errors import (
    RegistryExistsError,
    RegistryFrozenError,
    RegistryKeyError,
)
from .typing import K, V


class Registry(
    MutableRegistryProtocol[K, V],
    Generic[K, V],
    ):
    """
    Generic registry.

    A reusable mapping container with freeze support.

    All registries in the framework should inherit from this
    class.
    """

    def __init__(
        self,
        values: Mapping[K, V] | None = None,
    ) -> None:

        self._values: dict[K, V] = dict(values or {})
        self._frozen = False

    # ---------------------------------------------------------
    # Properties
    # ---------------------------------------------------------

    @property
    def frozen(self) -> bool:
        return self._frozen

    @property
    def is_empty(self) -> bool:
        return not self._values

    # ---------------------------------------------------------
    # Lifecycle
    # ---------------------------------------------------------

    def freeze(self) -> Self:
        """
        Prevent further modifications.
        """
        self._frozen = True
        return self

    def copy(self) -> Self:
        """
        Create a shallow copy of this registry.
        """
        registry = type(self)(self._values)

        if self._frozen:
            registry.freeze()

        return registry

    # ---------------------------------------------------------
    # CRUD
    # ---------------------------------------------------------

    def register(
        self,
        key: K,
        value: V,
    ) -> None:

        self._ensure_mutable()

        if key in self._values:
            raise RegistryExistsError(
                f"{key!r} is already registered."
            )

        self._values[key] = value

    def register_if_absent(
        self,
        key: K,
        value: V,
    ) -> V:

        if key not in self._values:
            self.register(key, value)

        return self._values[key]

    def register_many(
        self,
        values: Mapping[K, V],
    ) -> None:

        for key, value in values.items():
            self.register(key, value)

    def replace(
        self,
        key: K,
        value: V,
    ) -> None:

        self._ensure_mutable()

        self._values[key] = value

    def update(
        self,
        values: Mapping[K, V],
    ) -> None:

        for key, value in values.items():
            self.replace(key, value)

    def unregister(
        self,
        key: K,
    ) -> V:

        self._ensure_mutable()

        try:
            return self._values.pop(key)

        except KeyError as exc:
            raise RegistryKeyError(
                f"{key!r} is not registered."
            ) from exc

    def clear(self) -> None:

        self._ensure_mutable()

        self._values.clear()

    # ---------------------------------------------------------
    # Lookup
    # ---------------------------------------------------------

    def get(
        self,
        key: K,
    ) -> V:

        try:
            return self._values[key]

        except KeyError as exc:
            raise RegistryKeyError(
                f"{key!r} is not registered."
            ) from exc

    def require(
        self,
        key: K,
    ) -> V:
        """
        Alias of get().
        """
        return self.get(key)

    def get_or_none(
        self,
        key: K,
    ) -> V | None:

        return self._values.get(key)

    def contains(
        self,
        key: K,
    ) -> bool:

        return key in self._values

    # ---------------------------------------------------------
    # Views
    # ---------------------------------------------------------

    def keys(self) -> KeysView[K]:

        return self._values.keys()

    def values(self) -> ValuesView[V]:

        return self._values.values()

    def items(self) -> ItemsView[K, V]:

        return self._values.items()

    # ---------------------------------------------------------
    # Internal
    # ---------------------------------------------------------

    def _ensure_mutable(self) -> None:

        if self._frozen:
            raise RegistryFrozenError(
                f"{type(self).__name__} is frozen."
            )

    # ---------------------------------------------------------
    # Magic
    # ---------------------------------------------------------

    def __getitem__(
        self,
        key: K,
    ) -> V:

        return self.get(key)

    def __contains__(
        self,
        key: object,
    ) -> bool:

        return key in self._values

    def __len__(self) -> int:

        return len(self._values)

    def __bool__(self) -> bool:

        return bool(self._values)

    def __iter__(
        self,
    ) -> Iterator[tuple[K, V]]:

        return iter(self._values.items())

    def __repr__(self) -> str:

        return (
            f"{type(self).__name__}"
            f"(size={len(self)}, "
            f"frozen={self._frozen})"
        )