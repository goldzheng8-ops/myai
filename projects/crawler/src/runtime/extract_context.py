

from dataclasses import dataclass, field
from typing import Any

from adapters.base import NodeAdapter, ResponseAdapter
from runtime.request_context import RequestContext


@dataclass(slots=True)
class ExtractContext:

    request: RequestContext

    response: ResponseAdapter

    node: NodeAdapter | None = None

    variables: dict[str, Any] = field(
        default_factory=dict,
    )

    def get(
        self,
        key: str,
        default: Any = None,
    ) -> Any:

        return self.variables.get(
            key,
            default,
        )

    def set(
        self,
        key: str,
        value: Any,
    ) -> None:

        self.variables[key] = value

    def update(
        self,
        values: dict[str, Any],
    ) -> None:

        self.variables.update(values)