from __future__ import annotations

from collections.abc import Callable, Iterable, Iterator, Mapping
from typing import Generic

from .errors import RegistryFrozenError
from .typing import K, V


class MultiRegistry(
    Generic[K, V],
):
    """
    Registry supporting one key -> multiple values.

    Internal storage:
        dict[K, list[V]]

    External view:
        tuple[V, ...]

    Duplicate values are not allowed.
    """

    def __init__(
        self,
        values: Mapping[K, Iterable[V]] | None = None,
    ) -> None:

        self._values: dict[K, list[V]] = {}

        if values is not None:
            for key, items in values.items():
                self.replace_all(key, items)

        self._frozen = False

    # ---------------------------------------------------------
    # State
    # ---------------------------------------------------------

    @property
    def frozen(self) -> bool:
        return self._frozen

    def freeze(self) -> MultiRegistry[K, V]:
        self._frozen = True
        return self

    def _ensure_mutable(self) -> None:
        if self._frozen:
            raise RegistryFrozenError(
                "Registry is frozen."
            )

    # ---------------------------------------------------------
    # Query
    # ---------------------------------------------------------

    def contains(
        self,
        key: K,
    ) -> bool:

        return key in self._values

    def contains_value(
        self,
        key: K,
        value: V,
    ) -> bool:

        return value in self._values.get(key, ())

    def get_all(
        self,
        key: K,
    ) -> tuple[V, ...]:

        try:
            return tuple(self._values[key])

        except KeyError as exc:
            raise LookupError(
                f"{key!r} is not registered."
            ) from exc

    def get(
        self,
        key: K,
    ) -> tuple[V, ...]:
        return self.get_all(key)

    def get_one(
        self,
        key: K,
    ) -> V:

        values = self.get_all(key)

        if len(values) != 1:
            raise LookupError(
                f"{key!r} expected exactly one value, "
                f"got {len(values)}."
            )

        return values[0]

    def try_get_one(
        self,
        key: K,
    ) -> V | None:

        values = self.get_or_empty(key)

        if not values:
            return None

        if len(values) != 1:
            raise LookupError(
                f"{key!r} expected exactly one value, "
                f"got {len(values)}."
            )

        return values[0]

    def first(
        self,
        key: K,
    ) -> V:

        values = self.get_all(key)

        return values[0]

    def last(
        self,
        key: K,
    ) -> V:

        values = self.get_all(key)

        return values[-1]

    def find(
        self,
        key: K,
        predicate: Callable[[V], bool],
    ) -> V | None:

        for value in self.get_or_empty(key):

            if predicate(value):
                return value

        return None

    def filter(
        self,
        key: K,
        predicate: Callable[[V], bool],
    ) -> tuple[V, ...]:

        return tuple(
            value
            for value in self.get_or_empty(key)
            if predicate(value)
        )

    def get_or_empty(
        self,
        key: K,
    ) -> tuple[V, ...]:

        return tuple(
            self._values.get(key, ())
        )

    # ---------------------------------------------------------
    # Modify
    # ---------------------------------------------------------

    def add(
        self,
        key: K,
        value: V,
    ) -> None:

        self._ensure_mutable()

        bucket = self._values.setdefault(
            key,
            [],
        )

        if value in bucket:
            raise ValueError(
                f"{value!r} already registered for {key!r}."
            )

        bucket.append(value)

    def extend(
        self,
        key: K,
        values: Iterable[V],
    ) -> None:

        self._ensure_mutable()

        incoming = list(values)

        # ---------- validate duplicates inside incoming ----------

        if len(incoming) != len(set(incoming)):
            raise ValueError(
                "Duplicate values detected."
            )

        bucket = self._values.get(key, [])

        duplicates = [
            value
            for value in incoming
            if value in bucket
        ]

        if duplicates:
            raise ValueError(
                f"Values already registered: {duplicates!r}"
            )

        # ---------- commit ----------

        if key not in self._values:
            self._values[key] = incoming

        else:
            bucket.extend(incoming)

    def replace_all(
        self,
        key: K,
        values: Iterable[V],
    ) -> None:

        self._ensure_mutable()

        incoming = list(values)

        if len(incoming) != len(set(incoming)):
            raise ValueError(
                "Duplicate values detected."
            )

        self._values[key] = incoming

    def discard(
        self,
        key: K,
        value: V,
    ) -> bool:

        self._ensure_mutable()

        bucket = self._values.get(key)

        if bucket is None:
            return False

        try:
            bucket.remove(value)

        except ValueError:
            return False

        if not bucket:
            del self._values[key]

        return True

    def remove(
        self,
        key: K,
        value: V,
    ) -> None:

        if not self.discard(
            key,
            value,
        ):
            raise LookupError(
                f"{value!r} is not registered for {key!r}."
            )

    def unregister(
        self,
        key: K,
    ) -> tuple[V, ...]:

        self._ensure_mutable()

        try:
            values = self._values.pop(key)

        except KeyError as exc:
            raise LookupError(
                f"{key!r} is not registered."
            ) from exc

        return tuple(values)

    def clear(
        self,
    ) -> None:

        self._ensure_mutable()

        self._values.clear()

    # ---------------------------------------------------------
    # Views
    # ---------------------------------------------------------

    def keys(
        self,
    ):

        return self._values.keys()

    def values(
        self,
    ) -> tuple[tuple[V, ...], ...]:

        return tuple(
            tuple(values)
            for values in self._values.values()
        )

    def items(
        self,
    ) -> tuple[
        tuple[K, tuple[V, ...]],
        ...,
    ]:

        return tuple(
            (
                key,
                tuple(values),
            )
            for key, values in self._values.items()
        )

    # ---------------------------------------------------------
    # Copy
    # ---------------------------------------------------------

    def copy(
        self,
    ) -> MultiRegistry[K, V]:

        registry = self.__class__()

        registry._values = {
            key: values.copy()
            for key, values in self._values.items()
        }

        return registry

    # ---------------------------------------------------------
    # Magic
    # ---------------------------------------------------------

    def __contains__(
        self,
        key: object,
    ) -> bool:

        return key in self._values

    def __len__(
        self,
    ) -> int:

        return len(self._values)

    def __iter__(
        self,
    ) -> Iterator[
        tuple[K, tuple[V, ...]]
    ]:

        for key, values in self._values.items():
            yield (
                key,
                tuple(values),
            )