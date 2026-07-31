

from typing import Generic, TypeVar

from core.registry.base import Registry

K = TypeVar("K")
H = TypeVar("H")

class DispatchTable(

    Registry[
        K,
        H,
    ],

    Generic[K, H],
):
    def dispatch(
        self,
        key: K,
    ) -> H:

        return self.get(key)