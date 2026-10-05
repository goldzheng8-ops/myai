from __future__ import annotations

from abc import ABC, abstractmethod
from datetime import datetime, timezone
from typing import Literal

from core.request.context import RequestContext
from core.request.middleware.auth.auth_provider.config import OAuth2CredentialsProviderConfig
from core.request.middleware.auth.auth_provider.oauth2.models import OAuth2TokenSet
from core.request.middleware.auth.auth_state_provider import BrowserAuthStateProvider
from core.request.middleware.auth.model import BrowserAuthState


BrowserStorage = Literal[
    "local_storage",
    "session_storage",
    "cookies",
]


class OAuth2InitialTokenLoader(ABC):

    @abstractmethod
    async def load(
        self,
        context: RequestContext,
    ) -> OAuth2TokenSet | None:
        raise NotImplementedError


class BrowserOAuth2InitialTokenLoader(
    OAuth2InitialTokenLoader,
):

    def __init__(
        self,
        auth_state_provider: BrowserAuthStateProvider,
        config: OAuth2CredentialsProviderConfig,
    ) -> None:
        self._auth_state_provider = auth_state_provider
        self._config = config

    @property
    def auth_state_provider(
        self,
    ) -> BrowserAuthStateProvider:
        return self._auth_state_provider

    @property
    def config(
        self,
    ) -> OAuth2CredentialsProviderConfig:
        return self._config

    async def load(
        self,
        context: RequestContext,
    ) -> OAuth2TokenSet | None:

        state = await self._auth_state_provider.get_state(
            context=context,
        )

        access_token = self._get_required_value(
            storage=self.config.access_token_storage,
            key=self.config.access_token_key,
            state=state,
            field_name="access token",
        )

        if access_token is None:
            return None

        refresh_token = self._get_optional_value(
            storage=self.config.refresh_token_storage,
            key=self.config.refresh_token_key,
            state=state,
            field_name="refresh token",
        )

        expires_at = self._get_expires_at(
            state=state,
        )

        token_type = self._get_optional_value(
            storage=self.config.token_type_storage,
            key=self.config.token_type_key,
            state=state,
            field_name="token type",
        )

        return OAuth2TokenSet(
            access_token=access_token,
            token_type=token_type or "Bearer",
            expires_at=expires_at,
            refresh_token=refresh_token,
        )

    @classmethod
    def _get_required_value(
        cls,
        *,
        storage: BrowserStorage,
        key: str,
        state: BrowserAuthState,
        field_name: str,
    ) -> str | None:

        value = cls._get_value(
            storage=storage,
            key=key,
            state=state,
        )

        if value is None:
            return None

        if not value:
            raise ValueError(
                f"Browser OAuth2 {field_name} is empty "
                f"in {storage!r} under key {key!r}.",
            )

        return value

    @classmethod
    def _get_optional_value(
        cls,
        *,
        storage: BrowserStorage | None,
        key: str | None,
        state: BrowserAuthState,
        field_name: str,
    ) -> str | None:

        if storage is None and key is None:
            return None

        if storage is None or key is None:
            raise ValueError(
                f"OAuth2 {field_name} storage and key "
                "must be configured together.",
            )

        value = cls._get_value(
            storage=storage,
            key=key,
            state=state,
        )

        if value is None:
            return None

        if not value:
            raise ValueError(
                f"Browser OAuth2 {field_name} is empty "
                f"in {storage!r} under key {key!r}.",
            )

        return value

    @staticmethod
    def _get_value(
        *,
        storage: BrowserStorage,
        key: str,
        state: BrowserAuthState,
    ) -> str | None:

        if storage == "local_storage":
            return state.local_storage.get(key)

        if storage == "session_storage":
            return state.session_storage.get(key)

        if storage == "cookies":
            return BrowserOAuth2InitialTokenLoader._get_cookie(
                state=state,
                name=key,
            )

        raise ValueError(
            f"Unsupported browser storage: {storage!r}",
        )

    @staticmethod
    def _get_cookie(
        *,
        state: BrowserAuthState,
        name: str,
    ) -> str | None:

        for cookie in state.cookies:
            if cookie.name == name:
                return cookie.value

        return None

    def _get_expires_at(
        self,
        *,
        state: BrowserAuthState,
    ) -> datetime | None:

        value = self._get_optional_value(
            storage=self.config.expires_at_storage,
            key=self.config.expires_at_key,
            state=state,
            field_name="expires_at",
        )

        if value is None:
            return None

        return self._parse_expires_at(value)

    @staticmethod
    def _parse_expires_at(
        value: str,
    ) -> datetime:

        value = value.strip()

        if not value:
            raise ValueError(
                "OAuth2 expires_at cannot be empty.",
            )

        try:
            timestamp = float(value)
        except ValueError:
            timestamp = None

        if timestamp is not None:
            return datetime.fromtimestamp(
                timestamp,
                tz=timezone.utc,
            )

        normalized = value

        if normalized.endswith("Z"):
            normalized = normalized[:-1] + "+00:00"

        try:
            result = datetime.fromisoformat(
                normalized,
            )
        except ValueError as exc:
            raise ValueError(
                f"Invalid OAuth2 expires_at value: {value!r}.",
            ) from exc

        if result.tzinfo is None:
            result = result.replace(
                tzinfo=timezone.utc,
            )

        return result.astimezone(
            timezone.utc,
        )