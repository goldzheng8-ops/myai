from __future__ import annotations

from dataclasses import dataclass
from collections.abc import Iterable, Iterator
from .accessor import ObjectAccessor


@dataclass(
    slots=True,
    frozen=True,
)
class RegisteredAccessor:

    accessor: ObjectAccessor

    priority: int = 0

class AccessorRegistry:
    """
    Registry of object accessors.

    Accessors are ordered by priority.

    Higher priority wins.
    """

    def __init__(
        self,
        accessors: Iterable[RegisteredAccessor] = (),
    ) -> None:

        self._accessors = list(
            accessors,
        )

        self._sort()

        self._frozen = False

    @property
    def frozen(
        self,
    ) -> bool:

        return self._frozen


    def freeze(
        self,
    ) -> "AccessorRegistry":

        self._frozen = True

        return self


    def _ensure_mutable(
        self,
    ) -> None:

        if self._frozen:

            raise RuntimeError(
                "AccessorRegistry is frozen."
            )

    def register(
        self,
        accessor: ObjectAccessor,
        *,
        priority: int = 0,
    ) -> None:

        self._ensure_mutable()

        if any(
            item.accessor is accessor
            for item in self._accessors
        ):
            raise ValueError(
                "Accessor already registered."
            )

        self._accessors.append(
            RegisteredAccessor(
                accessor=accessor,
                priority=priority,
            )
        )

        self._sort()

    def unregister(
        self,
        accessor: ObjectAccessor,
    ) -> None:

        self._ensure_mutable()

        for index, item in enumerate(
            self._accessors,
        ):

            if item.accessor is accessor:

                del self._accessors[index]

                return

        raise LookupError(
            "Accessor not registered."
        )

    def contains(
        self,
        accessor: ObjectAccessor,
    ) -> bool:

        return any(
            item.accessor is accessor
            for item in self._accessors
        )

    def clear(
        self,
    ) -> None:

        self._ensure_mutable()

        self._accessors.clear()

    def accessors(
        self,
    ) -> tuple[ObjectAccessor, ...]:

        return tuple(
            item.accessor
            for item in self._accessors
        )

    def registered(
        self,
    ) -> tuple[
        RegisteredAccessor,
        ...,
    ]:

        return tuple(
            self._accessors
        )

    def copy(
        self,
    ) -> "AccessorRegistry":

        registry = AccessorRegistry(
            self._accessors,
        )

        return registry

    def __len__(
        self,
    ) -> int:

        return len(
            self._accessors,
        )

    def __iter__(
        self,
    ) -> Iterator[
        ObjectAccessor
    ]:

        for item in self._accessors:

            yield item.accessor

    def _sort(
        self,
    ) -> None:

        self._accessors.sort(
            key=lambda item: item.priority,
            reverse=True,
        )
