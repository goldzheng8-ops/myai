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