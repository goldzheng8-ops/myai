from collections.abc import Mapping
from typing import Any

from core.output.sink.base import OutputSink


class OutputResolver:

    def __init__(
        self,
        outputs: Mapping[str, OutputSink[Any]],
    ) -> None:
        self._outputs = dict(outputs)

    def resolve(
        self,
        name: str,
    ) -> OutputSink[Any]:
        try:
            return self._outputs[name]
        except KeyError as exc:
            raise LookupError(
                f"Output sink not found: {name!r}",
            ) from exc

    def contains(
        self,
        name: str,
    ) -> bool:
        return name in self._outputs

    def names(
        self,
    ) -> tuple[str, ...]:
        return tuple(self._outputs)

    def values(
        self,
    ) -> tuple[OutputSink[Any], ...]:
        return tuple(self._outputs.values())