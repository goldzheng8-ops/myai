from __future__ import annotations

from core.request.context import RequestContext
from core.request.middleware.base import RequestMiddleware
from core.request.middleware.typing import RequestMiddlewareNext

from .policy import CookiePolicy
from ..session.model import Session
from ..session.middleware import SESSION_RUNTIME_KEY


class CookieMiddleware(RequestMiddleware):

    def __init__(
        self,
        policy: CookiePolicy | None = None,
    ) -> None:

        self._policy = (
            policy
            if policy is not None
            else CookiePolicy()
        )

    @property
    def policy(self) -> CookiePolicy:
        return self._policy

    async def process(
        self,
        context: RequestContext,
        next_: RequestMiddlewareNext,
    ) -> RequestContext:

        if not self._policy.enabled:
            return await next_(context)

        self._inject_session_cookies(
            context,
        )

        result = await next_(
            context,
        )

        if self._policy.update_session_cookies:
            self._update_session_cookies(
                context,
            )

        return result

    def _get_session(
        self,
        context: RequestContext,
    ) -> Session | None:

        value = context.runtime.get(
            SESSION_RUNTIME_KEY,
        )

        if value is None:
            return None

        if not isinstance(value, Session):
            raise TypeError(
                f"Runtime value "
                f"{SESSION_RUNTIME_KEY!r} "
                "must be Session."
            )

        return value

    def _inject_session_cookies(
        self,
        context: RequestContext,
    ) -> None:

        if not self._policy.merge_session_cookies:
            return

        session = self._get_session(
            context,
        )

        if session is None:
            return

        request_cookies = (
            context.descriptor.cookies
        )

        for name, value in session.cookies.items():

            request_cookies.setdefault(
                name,
                value,
            )

    def _update_session_cookies(
        self,
        context: RequestContext,
    ) -> None:
        ...