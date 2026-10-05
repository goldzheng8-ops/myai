from typing import Generic

from .base import Registry
from .typing import K, H

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