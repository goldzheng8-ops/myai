from __future__ import annotations
from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class SessionPolicy:

    enabled: bool = True

    default_session_id: str | None = None

    create_if_missing: bool = True

    save_after_request: bool = True