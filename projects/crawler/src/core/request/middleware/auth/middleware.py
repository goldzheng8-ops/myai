from __future__ import annotations

from collections.abc import Mapping
from typing import TypeVar

from core.request.builder import RequestBuilder
from core.request.context import RequestContext
from core.request.middleware.base import RequestMiddleware
from core.request.middleware.config import MiddlewareConfig
from core.request.middleware.typing import RequestMiddlewareNext
from core.request.patch import RequestPatch

from .policy import AuthPolicy
from .provider import AuthCredentials, AuthProvider

T = TypeVar("T")

class AuthMiddleware(
    RequestMiddleware,
):

    def __init__(
        self,
        provider: AuthProvider,
        policy: AuthPolicy,
        config: MiddlewareConfig | None = None,
    ) -> None:
        super().__init__(
            config
            if config is not None
            else MiddlewareConfig(),
        )

        self._provider = provider

        self._policy = policy
    @property
    def provider(
        self,
    ) -> AuthProvider:

        return self._provider

    @property
    def policy(
        self,
    ) -> AuthPolicy:

        return self._policy

    async def process(
        self,
        context: RequestContext,
        next_: RequestMiddlewareNext,
    ) -> RequestContext:

        if not self._policy.enabled:
            return await next_(
                context,
            )

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

        headers = self._merge_mapping(
            descriptor.headers,
            credentials.headers,
            override=self._policy.override_headers,
        )

        cookies = self._merge_mapping(
            descriptor.cookies,
            credentials.cookies,
            override=self._policy.override_cookies,
        )

        params = self._merge_mapping(
            descriptor.params,
            credentials.params,
            override=self._policy.override_params,
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