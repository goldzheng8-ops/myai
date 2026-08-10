from __future__ import annotations

from dataclasses import dataclass
from typing import FrozenSet

from core.request.typing import HttpMethod


@dataclass(frozen=True, slots=True)
class CachePolicy:
    """
    Policy controlling request caching.
    """

    enabled: bool = True

    read: bool = True

    write: bool = True

    methods: FrozenSet[HttpMethod] = frozenset(
        {
            HttpMethod.GET,
            HttpMethod.HEAD,
        }
    )

    def allows(
        self,
        method: HttpMethod,
    ) -> bool:

        return (
            self.enabled
            and method in self.methods
        )