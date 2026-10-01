from datetime import datetime, timedelta, timezone
from typing import Any, Mapping, NoReturn
from core.request.middleware.auth.auth_provider.oauth2.errors import OAuth2HTTPError, OAuth2ProtocolError, OAuth2TokenError, OAuth2TransportError
import httpx

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

    @property
    def config(
        self,
    ) -> OAuth2TokenEndpointConfig:
        return self._config

    async def request_token(
        self,
        *,
        grant_type: str,
        parameters: Mapping[str, str] | None = None,
        scope: str | None = None,
    ) -> OAuth2TokenSet:

        data: dict[str, str] = {
            "grant_type": grant_type,
        }

        if parameters is not None:
            for key, value in parameters.items():
                if key in data:
                    raise ValueError(
                        f"OAuth2 parameter {key!r} "
                        "must not be specified twice.",
                    )

                data[key] = value

        if scope is not None:
            if "scope" in data:
                raise ValueError(
                    "OAuth2 scope must not be specified twice.",
                )

            data["scope"] = scope

        headers: dict[str, str] = {
            "Accept": "application/json",
        }

        auth = self._apply_client_auth(
            data=data,
            headers=headers,
        )

        response = await self._post(
            data=data,
            headers=headers,
            auth=auth,
        )

        return self._parse_response(
            response,
        )

    async def refresh_token(
        self,
        *,
        refresh_token: str,
        scope: str | None = None,
    ) -> OAuth2TokenSet:

        return await self.request_token(
            grant_type="refresh_token",
            parameters={
                "refresh_token": refresh_token,
            },
            scope=scope,
        )

    async def authorization_code(
        self,
        *,
        code: str,
        redirect_uri: str | None = None,
        scope: str | None = None,
    ) -> OAuth2TokenSet:

        parameters: dict[str, str] = {
            "code": code,
        }

        if redirect_uri is not None:
            parameters["redirect_uri"] = redirect_uri

        return await self.request_token(
            grant_type="authorization_code",
            parameters=parameters,
            scope=scope,
        )

    def _apply_client_auth(
        self,
        *,
        data: dict[str, str],
        headers: dict[str, str],
    ) -> httpx.BasicAuth | None:

        method = self._config.client_auth_method

        if method == "none":
            self._validate_public_client()

            client_id = self._config.client_id

            if client_id is not None:
                data["client_id"] = client_id

            return None

        if method == "client_secret_basic":
            return self._build_basic_auth()

        if method == "client_secret_post":
            self._apply_client_secret_post(
                data=data,
            )
            return None

        raise ValueError(
            "Unsupported OAuth2 client authentication method: "
            f"{method!r}",
        )

    def _validate_public_client(
        self,
    ) -> None:

        if self._config.client_id is None:
            raise ValueError(
                "client_id is required when "
                "client_auth_method='none'.",
            )

        if self._config.client_secret is not None:
            raise ValueError(
                "client_secret must not be configured when "
                "client_auth_method='none'.",
            )

    def _build_basic_auth(
        self,
    ) -> httpx.BasicAuth:

        client_id = self._config.client_id
        client_secret = self._config.client_secret

        if client_id is None:
            raise ValueError(
                "client_id is required for "
                "client_secret_basic.",
            )

        if client_secret is None:
            raise ValueError(
                "client_secret is required for "
                "client_secret_basic.",
            )

        return httpx.BasicAuth(
            username=client_id,
            password=client_secret,
        )

    def _apply_client_secret_post(
        self,
        *,
        data: dict[str, str],
    ) -> None:

        client_id = self._config.client_id
        client_secret = self._config.client_secret

        if client_id is None:
            raise ValueError(
                "client_id is required for "
                "client_secret_post.",
            )

        if client_secret is None:
            raise ValueError(
                "client_secret is required for "
                "client_secret_post.",
            )

        data["client_id"] = client_id
        data["client_secret"] = client_secret

    async def _post(
        self,
        *,
        data: Mapping[str, str],
        headers: Mapping[str, str],
        auth: httpx.BasicAuth | None,
    ) -> httpx.Response:
        try:
            if auth is None:
                return await self._client.post(
                    self._config.token_url,
                    data=data,
                    headers=headers,
                    timeout=self._config.timeout,
                )

            return await self._client.post(
                self._config.token_url,
                data=data,
                headers=headers,
                auth=auth,
                timeout=self._config.timeout,
            )

        except httpx.TimeoutException as exc:
            raise OAuth2TransportError(
                "OAuth2 token endpoint request timed out.",
            ) from exc

        except httpx.HTTPError as exc:
            raise OAuth2TransportError(
                "OAuth2 token endpoint request failed.",
            ) from exc
        
    def _parse_response(
        self,
        response: httpx.Response,
    ) -> OAuth2TokenSet:

        payload = self._parse_json(
            response,
        )

        if response.is_error:
            self._raise_token_error(
                response=response,
                payload=payload,
            )

        return self._parse_success_response(
            response=response,
            payload=payload,
        )

    @staticmethod
    def _parse_json(
        response: httpx.Response,
    ) -> Mapping[str, Any]:

        try:
            payload = response.json()

        except ValueError as exc:
            raise OAuth2ProtocolError(
                "OAuth2 token endpoint returned invalid JSON.",
            ) from exc

        if not isinstance(payload, dict):
            raise OAuth2ProtocolError(
                "OAuth2 token endpoint JSON response "
                "must be an object.",
            )

        return payload

    @staticmethod
    def _raise_token_error(
        *,
        response: httpx.Response,
        payload: Mapping[str, Any],
    ) -> NoReturn:

        error = payload.get("error")

        if not isinstance(error, str):
            raise OAuth2HTTPError(
                status_code=response.status_code,
                message=(
                    "OAuth2 token endpoint returned HTTP "
                    f"{response.status_code} without a valid "
                    "OAuth2 error code."
                ),
            )

        error_description = payload.get(
            "error_description",
        )

        if not isinstance(error_description, str):
            error_description = None

        error_uri = payload.get(
            "error_uri",
        )

        if not isinstance(error_uri, str):
            error_uri = None

        raise OAuth2TokenError(
            error=error,
            error_description=error_description,
            error_uri=error_uri,
            status_code=response.status_code,
        )

    @staticmethod
    def _parse_success_response(
        *,
        response: httpx.Response,
        payload: Mapping[str, Any],
    ) -> OAuth2TokenSet:

        access_token = payload.get(
            "access_token",
        )

        if not isinstance(access_token, str):
            raise OAuth2ProtocolError(
                "OAuth2 token endpoint success response "
                "does not contain a valid access_token.",
            )

        token_type = payload.get(
            "token_type",
        )

        if not isinstance(token_type, str):
            raise OAuth2ProtocolError(
                "OAuth2 token endpoint success response "
                "does not contain a valid token_type.",
            )

        expires_at = (
            OAuth2TokenEndpointClient._parse_expires_at(
                payload.get("expires_in"),
            )
        )

        refresh_token = payload.get(
            "refresh_token",
        )

        if (
            refresh_token is not None
            and not isinstance(refresh_token, str)
        ):
            raise OAuth2ProtocolError(
                "OAuth2 token endpoint returned an invalid "
                "refresh_token.",
            )

        scope = payload.get(
            "scope",
        )

        if (
            scope is not None
            and not isinstance(scope, str)
        ):
            raise OAuth2ProtocolError(
                "OAuth2 token endpoint returned an invalid scope.",
            )

        return OAuth2TokenSet(
            access_token=access_token,
            token_type=token_type,
            expires_at=expires_at,
            refresh_token=refresh_token,
            scope=scope,
        )

    @staticmethod
    def _parse_expires_at(
        value: Any,
    ) -> datetime | None:

        if value is None:
            return None

        if isinstance(value, bool):
            raise OAuth2ProtocolError(
                "OAuth2 expires_in must be numeric.",
            )

        try:
            seconds = float(value)

        except (TypeError, ValueError) as exc:
            raise OAuth2ProtocolError(
                "OAuth2 expires_in must be numeric.",
            ) from exc

        if seconds < 0:
            raise OAuth2ProtocolError(
                "OAuth2 expires_in must not be negative.",
            )

        return (
            datetime.now(timezone.utc)
            + timedelta(seconds=seconds)
        )