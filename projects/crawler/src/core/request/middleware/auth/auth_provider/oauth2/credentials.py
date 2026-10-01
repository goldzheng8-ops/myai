from datetime import datetime, timezone
from typing import Literal

from core.request.context import RequestContext
from core.request.middleware.auth.auth_provider.base import AuthCredentials, BaseAuthProvider
from core.request.middleware.auth.auth_provider.config import OAuth2CredentialsProviderConfig
from core.request.middleware.auth.auth_provider.oauth2.models import OAuth2TokenSet
from core.request.middleware.auth.auth_provider.oauth2.refresher import OAuth2TokenRefresher
from core.request.middleware.auth.auth_provider.oauth2.store import OAuth2TokenStore
from core.request.middleware.auth.auth_state_provider import BrowserAuthStateProvider
from core.request.middleware.auth.model import BrowserAuthState


class OAuth2CredentialsProvider(
    BaseAuthProvider[
        OAuth2CredentialsProviderConfig
    ],
):

    def __init__(
        self,
        auth_state_provider: BrowserAuthStateProvider,
        token_store: OAuth2TokenStore,
        token_refresher: OAuth2TokenRefresher,
        config: OAuth2CredentialsProviderConfig,
    ) -> None:
        super().__init__(config)

        self._auth_state_provider = auth_state_provider
        self._token_store = token_store
        self._token_refresher = token_refresher

    async def get(
        self,
        context: RequestContext,
    ) -> AuthCredentials:

        key = self._build_store_key(context)

        token_set = await self._get_or_initialize_token(
            context=context,
            key=key,
        )

        token_set = await self._ensure_valid_token(
            context=context,
            key=key,
            token_set=token_set,
        )

        return AuthCredentials(
            headers={
                "Authorization": (
                    f"{token_set.token_type} "
                    f"{token_set.access_token}"
                ),
            },
        )

    async def _get_or_initialize_token(
        self,
        *,
        context: RequestContext,
        key: str,
    ) -> OAuth2TokenSet:

        existing = await self._token_store.get(key)

        if existing is not None:
            return existing

        state = await self._auth_state_provider.get_state(
            context=context,
        )

        access_token = self._get_state_value(
            state=state,
            storage=self._config.access_token_storage,
            key=self._config.access_token_key,
        )

        if access_token is None:
            raise ValueError(
                "OAuth2 access token with key "
                f"'{self._config.access_token_key}' "
                "was not found.",
            )

        refresh_token: str | None = None

        if (
            self._config.refresh_token_storage is not None
            and self._config.refresh_token_key is not None
        ):
            refresh_token = self._get_state_value(
                state=state,
                storage=self._config.refresh_token_storage,
                key=self._config.refresh_token_key,
            )

        token_set = OAuth2TokenSet(
            access_token=access_token,
            refresh_token=refresh_token,
        )

        await self._token_store.set(
            key,
            token_set,
        )

        return token_set

    @staticmethod
    def _get_state_value(
        *,
        state: BrowserAuthState,
        storage: Literal[
            "local_storage",
            "session_storage",
            "cookies",
        ],
        key: str,
    ) -> str | None:

        if storage == "local_storage":
            return state.local_storage.get(key)

        if storage == "session_storage":
            return state.session_storage.get(key)

        if storage == "cookies":
            for cookie in state.cookies:
                if cookie.name == key:
                    return cookie.value

            return None

        raise ValueError(
            f"Unsupported OAuth2 storage: {storage!r}",
        )

    async def _ensure_valid_token(
        self,
        *,
        context: RequestContext,
        key: str,
        token_set: OAuth2TokenSet,
    ) -> OAuth2TokenSet:

        if not token_set.is_expired(
            now=datetime.now(timezone.utc),
            leeway=self._config.refresh_leeway,
        ):
            return token_set

        return await self._token_refresher.refresh(
            key=key,
            token_set=token_set,
        )

    def _build_store_key(
        self,
        context: RequestContext,
    ) -> str:

        session_id = context.session_id

        if session_id is None:
            raise ValueError(
                "OAuth2 authentication requires a session_id.",
            )

        return (
            f"{session_id}:"
            f"{self._config.provider_name}"
        )