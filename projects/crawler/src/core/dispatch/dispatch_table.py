

from typing import Generic, TypeVar

from registry.base import Registry

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