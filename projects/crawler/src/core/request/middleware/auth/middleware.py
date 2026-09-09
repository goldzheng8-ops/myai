from __future__ import annotations


from typing import Any, TypeVar

from core.request.builder import RequestBuilder
from core.request.context import RequestContext
from core.request.middleware.base import RequestMiddleware
from core.request.middleware.config import AuthMiddlewareConfig
from core.request.middleware.typing import MiddlewareType, RequestMiddlewareNext
from .provider import AuthCredentials, AuthProvider

T = TypeVar("T")

class AuthMiddleware(
    RequestMiddleware[AuthMiddlewareConfig],
):
    plugin_type = MiddlewareType.AUTH

    def __init__(
        self,
        provider: AuthProvider[Any],
        config: AuthMiddlewareConfig,
    ) -> None:
        super().__init__(config)

        self._provider = provider

    @property
    def provider(self) -> AuthProvider[Any]:
        return self._provider

    @property
    def config(self) -> AuthMiddlewareConfig:
        return self._config

    async def process(
        self,
        context: RequestContext,
        next_: RequestMiddlewareNext,
    ) -> RequestContext:

        credentials = await self._provider.get(
            context,
        )

        if credentials is not None:
            self._apply_credentials(
                context,
                credentials,
            )

        return await next_(context)

    def _apply_credentials(
        self,
        context: RequestContext,
        credentials: AuthCredentials,
    ) -> None:

        builder = RequestBuilder.from_descriptor(
            context.descriptor,
        )

        config = self.config

        if credentials.headers:
            builder.merge_headers(
                credentials.headers,
                override=config.override_headers,
            )

        if credentials.cookies:
            builder.merge_cookies(
                credentials.cookies,
                override=config.override_cookies,
            )

        if credentials.params:
            builder.merge_params(
                credentials.params,
                override=config.override_params,
            )

        context.descriptor = builder.build()