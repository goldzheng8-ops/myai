from dataclasses import dataclass, field
from typing import Mapping

from core.request.middleware.cookie.model import Cookie


@dataclass(frozen=True, slots=True)
class BrowserAuthState:
    cookies: tuple[Cookie, ...] = ()
    local_storage: Mapping[str, str] = field(
        default_factory=dict,
    )
    session_storage: Mapping[str, str] = field(
        default_factory=dict,
    )