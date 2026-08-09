from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True)
class Session:
    """
    Runtime state associated with a logical session.
    """

    id: str

    cookies: dict[str, str] = field(
        default_factory=dict,
    )

    metadata: dict[str, object] = field(
        default_factory=dict,
    )