from __future__ import annotations

from dataclasses import dataclass, field

from core.request.middleware.cookie.model import CookieJar


@dataclass(slots=True)
class Session:
    """
    Runtime state associated with a logical session.
    """

    id: str

    cookies: CookieJar = field(
        default_factory=CookieJar,
    )

    metadata: dict[str, object] = field(
        default_factory=dict,
    )