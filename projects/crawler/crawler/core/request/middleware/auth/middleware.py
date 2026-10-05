from __future__ import annotations


from typing import TypeVar

from core.request.builder import RequestBuilder
from core.request.context import RequestContext
from core.request.middleware.auth.auth_provider.registry import AuthProviderRegistry
from core.request.middleware.base import RequestMiddleware
from core.request.middleware.config import AuthMiddlewareConfig
from core.request.middleware.typing import MiddlewareType, RequestMiddlewareNext
from .auth_provider.base import AuthCredentials

T = TypeVar("T")

class AuthMiddleware(
    RequestMiddleware[AuthMiddlewareConfig],
):
    """
    Authentication credential propagation middleware.

    This middleware injects existing authentication
    credentials into outgoing requests.

    Interactive authentication is handled by the
    browser interaction layer.
    """
    plugin_type = MiddlewareType.AUTH

    def __init__(
        self,
        provider: AuthProviderRegistry,
        config: AuthMiddlewareConfig,
    ) -> None:
        super().__init__(config)

        self._provider = provider

    @property
    def provider(self) -> AuthProviderRegistry:
        return self._provider

    @property
    def config(self) -> AuthMiddlewareConfig:
        return self._config

    async def process(
        self,
        context: RequestContext,
        next_: RequestMiddlewareNext,
    ) -> RequestContext:

        credentials = await self._provider.resolve(self.config.provider).get(
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