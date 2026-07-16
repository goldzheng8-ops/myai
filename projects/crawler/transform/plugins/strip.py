

from typing import Any

from transform.base import TransformPlugin


class StripTransform(TransformPlugin):
    name = "strip"

    def apply(self, value: Any, **kwargs) -> Any:
        if isinstance(value, str):
            return value.strip()
        return value