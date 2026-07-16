

from typing import Any

from transform.base import TransformPlugin


class ReplaceTransform(TransformPlugin):
    name = "replace"

    def apply(self, value: Any, **kwargs) -> Any:
        if isinstance(value, str):
            old = kwargs.get("old", "")
            new = kwargs.get("new", "")
            return value.replace(old, new)
        return value