import asyncio

from core.request.middleware.auth.auth_provider.oauth2.endpoint import OAuth2TokenEndpointClient
from core.request.middleware.auth.auth_provider.oauth2.models import OAuth2TokenSet
from core.request.middleware.auth.auth_provider.oauth2.store import OAuth2TokenStore


class OAuth2TokenRefresher:

    def __init__(
        self,
        endpoint_client: OAuth2TokenEndpointClient,
        token_store: OAuth2TokenStore,
    ) -> None:
        self._endpoint_client = endpoint_client
        self._token_store = token_store
        self._locks: dict[str, asyncio.Lock] = {}
        self._locks_guard = asyncio.Lock()

    async def _get_lock(
        self,
        key: str,
    ) -> asyncio.Lock:

        async with self._locks_guard:
            lock = self._locks.get(key)

            if lock is None:
                lock = asyncio.Lock()
                self._locks[key] = lock

            return lock 

    async def refresh(
        self,
        *,
        key: str,
        token_set: OAuth2TokenSet,
    ) -> OAuth2TokenSet:

        lock = await self._get_lock(key)

        async with lock:

            current = await self._token_store.get(key)

            if current is not None:
                if (
                    current.access_token
                    != token_set.access_token
                ):
                    return current

            refresh_token = (
                current.refresh_token
                if current is not None
                else token_set.refresh_token
            )

            if refresh_token is None:
                raise ValueError(
                    "OAuth2 token cannot be refreshed because "
                    "no refresh_token is available.",
                )

            refreshed = (
                await self._endpoint_client.refresh_token(
                    refresh_token=refresh_token,
                )
            )

            await self._token_store.set(
                key,
                refreshed,
            )

            return refreshed   