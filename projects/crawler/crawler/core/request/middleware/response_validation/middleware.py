from __future__ import annotations

from core.request.context import RequestContext
from core.request.middleware.base import RequestMiddleware
from core.request.middleware.config import ResponseValidationMiddlewareConfig
from core.request.middleware.response_validation.exceptions import ResponseValidationError
from core.request.middleware.response_validation.validator import ResponseValidator
from core.request.middleware.typing import MiddlewareType, RequestMiddlewareNext

class ResponseValidationMiddleware(
    RequestMiddleware[
        ResponseValidationMiddlewareConfig,
    ],
):

    plugin_type = MiddlewareType.RESPONSE_VALIDATION

    def __init__(
        self,
        validator: ResponseValidator,
        config: ResponseValidationMiddlewareConfig,
    ) -> None:

        super().__init__(
            config,
        )

        self._validator = validator

    @property
    def validator(self) -> ResponseValidator:
        return self._validator

    @property
    def config(
        self,
    ) -> ResponseValidationMiddlewareConfig:
        return self._config

    async def process(
        self,
        context: RequestContext,
        next_: RequestMiddlewareNext,
    ) -> RequestContext:

        context = await next_(
            context,
        )

        result = context.result

        if result is None:
            raise ResponseValidationError(
                url=context.descriptor.url,
                reason=(
                    "Request executor produced "
                    "no RequestResult."
                ),
            )

        self._validator.validate(
            result,
        )

        return context