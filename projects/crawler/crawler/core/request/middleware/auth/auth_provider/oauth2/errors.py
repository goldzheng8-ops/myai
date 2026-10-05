class OAuth2Error(Exception):
    """Base OAuth2 exception."""


class OAuth2TokenEndpointError(OAuth2Error):
    """Base token endpoint exception."""


class OAuth2TransportError(
    OAuth2TokenEndpointError,
):
    """HTTP transport failed before a valid response was received."""


class OAuth2HTTPError(
    OAuth2TokenEndpointError,
):
    """Token endpoint returned an unexpected HTTP response."""

    def __init__(
        self,
        *,
        status_code: int,
        message: str,
    ) -> None:
        super().__init__(message)
        self.status_code = status_code


class OAuth2ProtocolError(
    OAuth2TokenEndpointError,
):
    """Token endpoint returned an invalid OAuth2 response."""


class OAuth2TokenError(
    OAuth2TokenEndpointError,
):
    """OAuth2 error response from the token endpoint."""

    def __init__(
        self,
        *,
        error: str,
        error_description: str | None = None,
        error_uri: str | None = None,
        status_code: int | None = None,
    ) -> None:
        message = (
            f"OAuth2 token endpoint error: {error}"
        )

        if error_description:
            message += f": {error_description}"

        super().__init__(message)

        self.error = error
        self.error_description = error_description
        self.error_uri = error_uri
        self.status_code = status_code


class OAuth2AuthenticationRequiredError(
    OAuth2Error,
):
    """
    The OAuth2 credential can no longer be refreshed.

    Interactive authentication or another credential
    acquisition flow is required.
    """

class OAuth2RefreshError(
    OAuth2Error,
):
    """
    Refresh operation failed without invalidating
    the current OAuth2 credential.
    """