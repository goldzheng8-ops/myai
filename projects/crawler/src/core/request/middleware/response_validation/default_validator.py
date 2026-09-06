from core.request.middleware.config import ResponseValidationMiddlewareConfig
from core.request.middleware.response_validation.exceptions import ResponseValidationError
from core.request.middleware.response_validation.validator import ResponseValidator
from core.request.result import RequestResult
from core.request.response.model import RequestResponse

class DefaultResponseValidator(
    ResponseValidator,
):

    def __init__(
        self,
        config: ResponseValidationMiddlewareConfig,
    ) -> None:
        self._config = config

    def validate(
        self,
        result: RequestResult,
    ) -> None:

        response = result.response

        if response is None:
            raise ResponseValidationError(
                url="",
                reason="Response is missing.",
            )

        self._validate_status(
            response,
        )

        self._validate_content_type(
            response,
        )

        self._validate_body_size(
            response,
        )

    def _validate_status(
        self,
        response: RequestResponse,
    ) -> None:

        status_codes = self._config.status_codes

        if status_codes is None:
            return

        if response.status_code in status_codes:
            return

        raise ResponseValidationError(
            url=response.url,
            reason=(
                f"unexpected status code "
                f"{response.status_code}; "
                f"expected one of "
                f"{sorted(status_codes)}"
            ),
        )

    def _validate_content_type(
        self,
        response: RequestResponse,
    ) -> None:

        content_types = self._config.content_types

        if content_types is None:
            return

        content_type = self._get_content_type(
            response,
        )

        if content_type is None:
            raise ResponseValidationError(
                url=response.url,
                reason="Missing Content-Type header.",
            )

        media_type = (
            content_type
            .split(";", 1)[0]
            .strip()
            .lower()
        )

        normalized = {
            value.lower()
            for value in content_types
        }

        if media_type in normalized:
            return

        raise ResponseValidationError(
            url=response.url,
            reason=(
                f"unexpected content type "
                f"{media_type!r}; "
                f"expected one of "
                f"{sorted(normalized)}"
            ),
        )

    def _validate_body_size(
        self,
        response: RequestResponse,
    ) -> None:

        size = len(response.body)

        minimum = self._config.min_body_size

        if (
            minimum is not None
            and size < minimum
        ):
            raise ResponseValidationError(
                url=response.url,
                reason=(
                    f"response body is too small: "
                    f"{size} < {minimum}"
                ),
            )

        maximum = self._config.max_body_size

        if (
            maximum is not None
            and size > maximum
        ):
            raise ResponseValidationError(
                url=response.url,
                reason=(
                    f"response body is too large: "
                    f"{size} > {maximum}"
                ),
            )

    @staticmethod
    def _get_content_type(
        response: RequestResponse,
    ) -> str | None:

        for name, value in response.headers.items():
            if name.lower() == "content-type":
                return value

        return None