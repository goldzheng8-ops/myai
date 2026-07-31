from typing import Generic, TypeVar

from .registry import Registry

K = TypeVar("K")
H = TypeVar("H")


class DispatchTable(
    Registry[K, H],
    Generic[K, H],
):
    """
    Dispatch table.

    Maps a key to a handler.

    Used by:

        ResponseAdapter

        Pipeline

        Resolver

        ValueEngine

        TransformEngine
    """

    def dispatch(
        self,
        key: K,
    ) -> H:

        return self.get(key)