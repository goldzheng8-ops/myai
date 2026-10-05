from dataclasses import dataclass
from datetime import datetime

from core.request.middleware.auth.auth_provider.oauth2.typing import OAuth2TokenState


@dataclass(frozen=True, slots=True, kw_only=True)
class OAuth2TokenSet:
    access_token: str
    token_type: str = "Bearer"
    expires_at: datetime | None = None
    refresh_token: str | None = None
    scope: str | None = None

    def is_expired(
        self,
        *,
        now: datetime,
        leeway: float = 0.0,
    ) -> bool:
        if self.expires_at is None:
            return False

        return now.timestamp() + leeway >= self.expires_at.timestamp()


@dataclass(frozen=True, slots=True, kw_only=True)
class OAuth2TokenRecord:
    token_set: OAuth2TokenSet | None
    state: OAuth2TokenState = OAuth2TokenState.ACTIVE
    invalid_reason: str | None = None