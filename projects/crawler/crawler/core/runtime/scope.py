from __future__ import annotations

from dataclasses import dataclass, field
from collections.abc import MutableMapping
from typing import Any


@dataclass(slots=True)
class RuntimeScope:
    """
    One variable scope.

    Examples
    --------
    Global
    Request
    Loop
    Template
    """

    values: MutableMapping[str, Any] = field(
        default_factory=dict,
    )

    name: str = ""

    readonly: bool = False

    def contains(
        self,
        name: str,
    ) -> bool:
        return name in self.values

    def get(
        self,
        name: str,
        default: Any = None,
    ) -> Any:
        return self.values.get(name, default)

    def set(
        self,
        name: str,
        value: Any,
    ) -> None:

        if self.readonly:
            raise RuntimeError(
                "Scope is readonly."
            )

        self.values[name] = value

    def remove(
        self,
        name: str,
    ) -> None:

        if self.readonly:
            raise RuntimeError(
                "Scope is readonly."
            )

        self.values.pop(name, None)

    def clear(self):
        if self.readonly:
            raise RuntimeError(
                "Scope is readonly."
            )
        self.values.clear()