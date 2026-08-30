from __future__ import annotations

from collections.abc import Mapping
from typing import TypeVar

from core.request.builder import RequestBuilder
from core.request.context import RequestContext
from core.request.middleware.base import RequestMiddleware
from core.request.middleware.config import AuthMiddlewareConfig
from core.request.middleware.typing import RequestMiddlewareNext
from core.request.patch import RequestPatch
from .provider import AuthCredentials, AuthProvider

T = TypeVar("T")

class AuthMiddleware(
    RequestMiddleware[AuthMiddlewareConfig],
):

    def __init__(
        self,
        provider: AuthProvider,
        config: AuthMiddlewareConfig,
    ) -> None:
        super().__init__(
            config
        )

        self._provider = provider
    @property
    def provider(
        self,
    ) -> AuthProvider:

        return self._provider
    @property
    def config(self) -> AuthMiddlewareConfig:
        return self._config
    
    async def process(
        self,
        context: RequestContext,
        next_: RequestMiddlewareNext,
    ) -> RequestContext:

        credentials = await self._provider.provide(
            context,
        )

        if credentials is not None:

            self._apply_credentials(
                context,
                credentials,
            )

        return await next_(
            context,
        )

    def _apply_credentials(
        self,
        context: RequestContext,
        credentials: AuthCredentials,
    ) -> None:

        descriptor = context.descriptor
        config = self.config

        headers = self._merge_mapping(
            descriptor.headers,
            credentials.headers,
            override=config.override_headers,
        )

        cookies = self._merge_mapping(
            descriptor.cookies,
            credentials.cookies,
            override=config.override_cookies,
        )

        params = self._merge_mapping(
            descriptor.params,
            credentials.params,
            override=config.override_params,
        )

        patch = RequestPatch(
            headers=headers,
            cookies=cookies,
            params=params,
        )

        context.descriptor = (
            RequestBuilder.from_patch(
                descriptor=descriptor,
                patch=patch,
            )
        )

    @staticmethod
    def _merge_mapping(
        existing: Mapping[str, T],
        credentials: Mapping[str, T],
        *,
        override: bool,
    ) -> dict[str, T]:

        result = dict(existing)

        if override:
            result.update(credentials)

        else:
            for name, value in credentials.items():
                result.setdefault(
                    name,
                    value,
                )

        return result