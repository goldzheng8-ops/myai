from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping


@dataclass(slots=True)
class EventContext:
    data: Mapping[str, Any]

    def get(self, key: str, default: Any = None) -> Any:
        return self.data.get(key, default)

    def __getitem__(self, key: str) -> Any:
        return self.data[key]

    def __contains__(self, key: object) -> bool:
        return key in self.data

    def __iter__(self):
        return iter(self.data.items())