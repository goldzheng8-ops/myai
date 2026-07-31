from collections.abc import Iterator, Mapping
from typing import Generic, TypeVar

K = TypeVar("K")
V = TypeVar("V")


class Registry(
    Generic[K, V],
):
    """
    Generic registry.

    Provides a reusable mapping container.

    All registries in the framework inherit from this class.
    """

    def __init__(
        self,
        values: Mapping[K, V] | None = None,
    ) -> None:

        self._values: dict[K, V] = dict(values or {})

    # ---------------------------------------------------------
    # CRUD
    # ---------------------------------------------------------

    def register(
        self,
        key: K,
        value: V,
    ) -> None:

        if key in self._values:
            raise ValueError(
                f"{key!r} already registered."
            )

        self._values[key] = value

    def replace(
        self,
        key: K,
        value: V,
    ) -> None:

        self._values[key] = value

    def get(
        self,
        key: K,
    ) -> V:

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

    def clear(self) -> None:
        self._values.clear()

    # ---------------------------------------------------------
    # Query
    # ---------------------------------------------------------

    def contains(
        self,
        key: K,
    ) -> bool:

        return key in self._values

    # ---------------------------------------------------------
    # Views
    # ---------------------------------------------------------

    def keys(self):
        return self._values.keys()

    def values(self):
        return self._values.values()

    def items(self):
        return self._values.items()

    # ---------------------------------------------------------
    # Magic
    # ---------------------------------------------------------

    def __contains__(
        self,
        key: object,
    ) -> bool:

        return key in self._values

    def __len__(self) -> int:

        return len(self._values)

    def __iter__(
        self,
    ) -> Iterator[tuple[K, V]]:

        return iter(self._values.items())