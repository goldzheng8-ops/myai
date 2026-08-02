from dataclasses import dataclass
from typing import Any, Mapping


@dataclass(slots=True, frozen=True)
class RequestPatch:

    url: str | None = None

    params: Mapping[str, Any] | None = None

    body: Any = None
