from __future__ import annotations

from collections.abc import Sequence
from typing import Protocol

from .accessor import ObjectAccessor


class AccessorProvider(
    Protocol,
):

    def accessors(
        self,
    ) -> Sequence[
        ObjectAccessor
    ]:
        ...

class DefaultAccessorProvider(
    AccessorProvider,
):

    def __init__(
        self,
        accessors: Sequence[ObjectAccessor],
    ) -> None:

        self._accessors = tuple(accessors)

    def accessors(
        self,
    ) -> Sequence[ObjectAccessor]:

        return self._accessors