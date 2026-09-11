
from __future__ import annotations

import asyncio
import time
from dataclasses import dataclass

from core.request.middleware.auth.config import OAuth2ClientCredentialsProviderConfig
from core.request.middleware.auth.exceptions import OAuth2AuthenticationError
import httpx

from core.request.context import RequestContext
from .provider import AuthCredentials, BaseAuthProvider




@dataclass(frozen=True, slots=True)
class OAuth2Token:

    access_token: str

    token_type: str = "Bearer"

    expires_at: float | None = None


class OAuth2ClientCredentialsProvider(
    BaseAuthProvider[OAuth2ClientCredentialsProviderConfig],
):

    def __init__(
        self,
        config:OAuth2ClientCredentialsProviderConfig
    ) -> None:
        super().__init__(config)

        self._client: httpx.AsyncClient | None = None
        self._token: OAuth2Token | None = None
        self._lock = asyncio.Lock()

    async def start(self) -> None:

        if self._client is not None:
            return

        self._client = httpx.AsyncClient(
            timeout=self.config.timeout,
        )

    async def get(
        self,
        context: RequestContext,
    ) -> AuthCredentials:

        client = self._require_client()

        token = await self._get_token(
            client,
        )

        return AuthCredentials(
            headers={
                "Authorization":
                    f"{token.token_type} "
                    f"{token.access_token}",
            },
        )

    async def _get_token(
        self,
        client: httpx.AsyncClient,
    ) -> OAuth2Token:

        token = self._token

        if (
            token is not None
            and not self._is_expired(token)
        ):
            return token

        async with self._lock:

            token = self._token

            if (
                token is not None
                and not self._is_expired(token)
            ):
                return token

            token = await self._request_token(
                client,
            )

            self._token = token

            return token

    def _is_expired(
        self,
        token: OAuth2Token,
    ) -> bool:

        if token.expires_at is None:
            return False

        return (
            time.monotonic()
            >= (
                token.expires_at
                - self.config.token_expiry_margin
            )
        )

    async def _request_token(
        self,
        client: httpx.AsyncClient,
    ) -> OAuth2Token:

        data: dict[str, str] = {
            "grant_type": "client_credentials",
        }

        if self.config.scope is not None:
            data["scope"] = self.config.scope

        response = await client.post(
            self.config.token_url,
            data=data,
            auth=(
                self.config.client_id,
                self.config.client_secret,
            ),
        )

        response.raise_for_status()

        payload = response.json()

        access_token = payload.get(
            "access_token",
        )

        if not isinstance(access_token, str):
            raise OAuth2AuthenticationError(
                "OAuth2 token response does not "
                "contain a valid access_token.",
            )

        token_type = payload.get(
            "token_type",
            "Bearer",
        )

        if not isinstance(token_type, str):
            token_type = "Bearer"

        expires_in = payload.get(
            "expires_in",
        )

        expires_at: float | None = None

        if isinstance(expires_in, int | float):
            expires_at = (
                time.monotonic()
                + float(expires_in)
            )

        return OAuth2Token(
            access_token=access_token,
            token_type=token_type,
            expires_at=expires_at,
        )

    def _require_client(
        self,
    ) -> httpx.AsyncClient:

        client = self._client

        if client is None:
            raise RuntimeError(
                "OAuth2ClientCredentialsProvider "
                "has not been started.",
            )

        return client

    async def close(self) -> None:

        client = self._client

        if client is None:
            return

        self._client = None
        self._token = None

        await client.aclose()