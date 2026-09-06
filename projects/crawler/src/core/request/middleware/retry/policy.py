import asyncio
from typing import Protocol

from core.request.context import RequestContext
from core.request.middleware.retry.config import RetryPolicyConfig
from core.request.middleware.retry.exceptions import NonRetryableError, RetryableError
from core.request.middleware.robot.exceptions import RobotsDenied
from core.request.middleware.response_validation.exceptions import ResponseValidationError
import httpx


class RetryPolicy(Protocol):

    def should_retry(
        self,
        *,
        context: RequestContext,
        exception: BaseException,
    ) -> bool:
        ...

class DefaultRetryPolicy:

    def __init__(
        self,
        config: RetryPolicyConfig,
    ) -> None:
        self._config = config

    def should_retry(
        self,
        *,
        context: RequestContext,
        exception: BaseException,
    ) -> bool:

        if isinstance(
            exception,
            asyncio.CancelledError,
        ):
            return False

        if isinstance(
            exception,
            RobotsDenied,
        ):
            return False

        if isinstance(
            exception,
            NonRetryableError,
        ):
            return False

        if isinstance(
            exception,
            RetryableError,
        ):
            return True

        if isinstance(
            exception,
            httpx.TransportError,
        ):
            return True

        if isinstance(
            exception,
            ResponseValidationError,
        ):
            status_code = exception.status_code

            if status_code is None:
                return False

            return (
                status_code
                in self._config.retry_status_codes
            )

        return False