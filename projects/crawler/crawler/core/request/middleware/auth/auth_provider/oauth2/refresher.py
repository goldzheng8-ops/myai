from __future__ import annotations
import asyncio
from datetime import datetime, timezone
from dataclasses import replace
from collections.abc import Awaitable, Callable

from core.request.middleware.auth.auth_provider.oauth2.endpoint import OAuth2TokenEndpointClient
from core.request.middleware.auth.auth_provider.oauth2.errors import OAuth2AuthenticationRequiredError, OAuth2RefreshError, OAuth2TokenEndpointError, OAuth2TokenError
from core.request.middleware.auth.auth_provider.oauth2.models import OAuth2TokenRecord, OAuth2TokenSet
from core.request.middleware.auth.auth_provider.oauth2.store import OAuth2TokenStore
from core.request.middleware.auth.auth_provider.oauth2.typing import OAuth2TokenState




OAuth2TokenLoader = Callable[
    [],
    Awaitable[OAuth2TokenSet | None],
]

class OAuth2TokenRefresher:

    def __init__(
        self,
        endpoint_client: OAuth2TokenEndpointClient,
        token_store: OAuth2TokenStore,
    ) -> None:

        self._endpoint_client = endpoint_client
        self._token_store = token_store

        self._locks: dict[
            tuple[str, str],
            asyncio.Lock,
        ] = {}

        self._locks_guard = asyncio.Lock()

    async def get_valid(
        self,
        *,
        session_id: str,
        key: str,
        initial_token_loader: OAuth2TokenLoader,
        leeway: float = 30.0,
    ) -> OAuth2TokenSet:

        lock = await self._get_lock(
            session_id=session_id,
            key=key,
        )

        async with lock:
            return await self._get_valid_locked(
                session_id=session_id,
                key=key,
                initial_token_loader=initial_token_loader,
                leeway=leeway,
            )

    async def _get_lock(
        self,
        *,
        session_id: str,
        key: str,
    ) -> asyncio.Lock:

        lock_key = (
            session_id,
            key,
        )

        async with self._locks_guard:
            lock = self._locks.get(
                lock_key,
            )

            if lock is None:
                lock = asyncio.Lock()
                self._locks[lock_key] = lock

            return lock

    async def _get_valid_locked(
        self,
        *,
        session_id: str,
        key: str,
        initial_token_loader: OAuth2TokenLoader,
        leeway: float,
    ) -> OAuth2TokenSet:

        record = await self._token_store.get(
            session_id=session_id,
            key=key,
        )

        if record is not None:
            if record.state == OAuth2TokenState.INVALID:
                raise OAuth2AuthenticationRequiredError(
                    self._invalid_message(record),
                )

            token_set = record.token_set

            if token_set is not None:
                if not token_set.is_expired(
                    now=datetime.now(timezone.utc),
                    leeway=leeway,
                ):
                    return token_set

                return await self._refresh_locked(
                    session_id=session_id,
                    key=key,
                    token_set=token_set,
                )

        token_set = await initial_token_loader()

        if token_set is None:
            raise OAuth2AuthenticationRequiredError(
                "No OAuth2 credentials are available "
                "for the current session.",
            )

        await self._token_store.set(
            session_id=session_id,
            key=key,
            token_set=token_set,
        )

        return token_set

    async def _refresh_locked(
        self,
        *,
        session_id: str,
        key: str,
        token_set: OAuth2TokenSet,
    ) -> OAuth2TokenSet:

        refresh_token = token_set.refresh_token

        if refresh_token is None:
            raise OAuth2AuthenticationRequiredError(
                "OAuth2 token cannot be refreshed because "
                "no refresh token is available.",
            )

        try:
            refreshed = (
                await self._endpoint_client.refresh_token(
                    refresh_token=refresh_token,
                    scope=token_set.scope,
                )
            )

        except OAuth2TokenError as exc:
            if exc.error == "invalid_grant":
                await self._token_store.invalidate(
                    session_id=session_id,
                    key=key,
                    reason=(
                        exc.error_description
                        or (
                            "OAuth2 refresh token was rejected "
                            "with invalid_grant."
                        )
                    ),
                )

                raise OAuth2AuthenticationRequiredError(
                    "OAuth2 refresh token is no longer valid."
                    + (
                        f" {exc.error_description}"
                        if exc.error_description
                        else ""
                    ),
                ) from exc

            raise OAuth2RefreshError(
                "OAuth2 token refresh failed: "
                f"{exc}",
            ) from exc

        except OAuth2TokenEndpointError as exc:
            raise OAuth2RefreshError(
                "OAuth2 token refresh failed.",
            ) from exc

        refreshed = self._apply_refresh_token_rotation(
            previous=token_set,
            refreshed=refreshed,
        )

        await self._token_store.set(
            session_id=session_id,
            key=key,
            token_set=refreshed,
        )

        return refreshed

    @staticmethod
    def _apply_refresh_token_rotation(
        *,
        previous: OAuth2TokenSet,
        refreshed: OAuth2TokenSet,
    ) -> OAuth2TokenSet:

        if refreshed.refresh_token is not None:
            return refreshed

        if previous.refresh_token is None:
            return refreshed

        return replace(
            refreshed,
            refresh_token=previous.refresh_token,
        )
    
    async def clear_session(
        self,
        session_id: str,
    ) -> None:

        await self._token_store.clear_session(
            session_id,
        )

        async with self._locks_guard:
            keys = tuple(
                lock_key
                for lock_key in self._locks
                if lock_key[0] == session_id
            )

            for lock_key in keys:
                self._locks.pop(
                    lock_key,
                    None,
                )

    @staticmethod
    def _invalid_message(
        record: OAuth2TokenRecord,
    ) -> str:
        if record.invalid_reason is None:
            return (
                "OAuth2 credentials have been invalidated."
            )

        return (
            "OAuth2 credentials have been invalidated. "
            f"Reason: {record.invalid_reason}"
        )