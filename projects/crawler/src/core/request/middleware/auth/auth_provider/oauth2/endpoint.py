from datetime import datetime, timedelta, timezone
from typing import Any, Mapping
import httpx
import base64

from core.request.middleware.auth.auth_provider.oauth2.models import OAuth2TokenSet
from core.request.middleware.auth.auth_provider.oauth2.config import OAuth2TokenEndpointConfig

class OAuth2TokenEndpointClient:

    def __init__(
        self,
        client: httpx.AsyncClient,
        config: OAuth2TokenEndpointConfig,
    ) -> None:
        self._client = client
        self._config = config

    async def refresh_token(
        self,
        *,
        refresh_token: str,
    ) -> OAuth2TokenSet:

        data: dict[str, str] = {
            "grant_type": "refresh_token",
            "refresh_token": refresh_token,
        }

        self._apply_client_auth(
            data=data,
            headers={},
        )

        response = await self._client.post(
            self._config.token_url,
            data=data,
            timeout=self._config.timeout,
        )

        response.raise_for_status()

        payload = response.json()

        return self._parse_token_response(
            payload,
            previous_refresh_token=refresh_token,
        )

    def _apply_client_auth(
        self,
        *,
        data: dict[str, str],
        headers: dict[str, str],
    ) -> None:

        config = self._config

        if config.client_auth_method == "client_secret_post":
            if config.client_id is not None:
                data["client_id"] = config.client_id

            if config.client_secret is not None:
                data["client_secret"] = config.client_secret

            return

        if config.client_auth_method == "client_secret_basic":
            if (
                config.client_id is None
                or config.client_secret is None
            ):
                raise ValueError(
                    "client_id and client_secret are required "
                    "for client_secret_basic.",
                )

            credentials = (
                f"{config.client_id}:{config.client_secret}"
            )

            encoded = base64.b64encode(
                credentials.encode("utf-8"),
            ).decode("ascii")

            headers["Authorization"] = (
                f"Basic {encoded}"
            )

            return

        raise ValueError(
            "Unsupported OAuth2 client authentication method: "
            f"{config.client_auth_method!r}",
        )



    @staticmethod
    def _parse_token_response(
        payload: Mapping[str, Any],
        *,
        previous_refresh_token: str | None = None,
    ) -> OAuth2TokenSet:

        access_token = payload.get("access_token")

        if not isinstance(access_token, str):
            raise ValueError(
                "OAuth2 token endpoint response does not contain "
                "a valid access_token.",
            )

        token_type = payload.get(
            "token_type",
            "Bearer",
        )

        if not isinstance(token_type, str):
            raise ValueError(
                "OAuth2 token endpoint returned an invalid "
                "token_type.",
            )

        expires_at: datetime | None = None

        expires_in = payload.get("expires_in")

        if expires_in is not None:
            try:
                seconds = float(expires_in)
            except (TypeError, ValueError) as exc:
                raise ValueError(
                    "OAuth2 token endpoint returned an invalid "
                    "expires_in.",
                ) from exc

            expires_at = (
                datetime.now(timezone.utc)
                + timedelta(seconds=seconds)
            )

        refresh_token = payload.get(
            "refresh_token",
        )

        if refresh_token is None:
            refresh_token = previous_refresh_token

        if not isinstance(refresh_token, str | None):
            raise ValueError(
                "OAuth2 token endpoint returned an invalid "
                "refresh_token.",
            )

        scope = payload.get("scope")

        if not isinstance(scope, str | None):
            raise ValueError(
                "OAuth2 token endpoint returned an invalid scope.",
            )

        return OAuth2TokenSet(
            access_token=access_token,
            token_type=token_type,
            expires_at=expires_at,
            refresh_token=refresh_token,
            scope=scope,
        )

    async def request_token(
        self,
        *,
        grant_type: str,
        parameters: Mapping[str, str],
    ) -> OAuth2TokenSet:
        ...