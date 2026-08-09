from __future__ import annotations

from core.request.context import RequestContext
from core.request.middleware.base import RequestMiddleware
from core.request.middleware.typing import RequestMiddlewareNext

from .policy import AuthPolicy
from .provider import AuthCredentials, AuthProvider


class AuthMiddleware(
    RequestMiddleware,
):

    def __init__(
        self,
        provider: AuthProvider,
        policy: AuthPolicy | None = None,
    ) -> None:

        self._provider = provider

        self._policy = (
            policy
            if policy is not None
            else AuthPolicy()
        )

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

        self._merge_headers(
            descriptor.headers,
            credentials.headers,
        )

        self._merge_cookies(
            descriptor.cookies,
            credentials.cookies,
        )

        self._merge_params(
            descriptor.params,
            credentials.params,
        )

    def _merge_headers(
        self,
        target: dict[str, str],
        source: dict[str, str],
    ) -> None:

        if self._policy.override_headers:

            target.update(source)

            return

        for name, value in source.items():

            target.setdefault(
                name,
                value,
            )

    def _merge_cookies(
        self,
        target: dict[str, str],
        source: dict[str, str],
    ) -> None:

        if self._policy.override_cookies:

            target.update(source)

            return

        for name, value in source.items():

            target.setdefault(
                name,
                value,
            )

    def _merge_params(
        self,
        target: dict[str, str],
        source: dict[str, str],
    ) -> None:

        if self._policy.override_params:

            target.update(source)

            return

        for name, value in source.items():

            target.setdefault(
                name,
                value,
            )