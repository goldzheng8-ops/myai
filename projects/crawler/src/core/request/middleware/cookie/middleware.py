from __future__ import annotations

from core.request.builder import RequestBuilder
from core.request.context import RequestContext
from core.request.middleware.base import RequestMiddleware
from core.request.middleware.config import CookieMiddlewareConfig
from core.request.middleware.typing import MiddlewareType, RequestMiddlewareNext


from ..session.middleware import SESSION_RUNTIME_KEY
from ..session.model import Session

class CookieMiddleware(
    RequestMiddleware[CookieMiddlewareConfig],
):
    """
    Manage request cookies through the current Session.

    CookieMiddleware does not own session state and does not
    persist sessions. SessionMiddleware is responsible for the
    session lifecycle and persistence.
    """
    plugin_type = MiddlewareType.COOKIE
    def __init__(
        self,
        config: CookieMiddlewareConfig,
    ) -> None:
        super().__init__(
            config
        )
    @property
    def config(self) -> CookieMiddlewareConfig:
        return self._config
    async def process(
        self,
        context: RequestContext,
        next_: RequestMiddlewareNext,
    ) -> RequestContext:
        config=self.config
        if config.merge_session_cookies:
            self._apply_session_cookies(
                context,
            )

        context = await next_(
            context,
        )

        if config.update_session_cookies:
            self._update_session_cookies(
                context,
            )

        return context

    # ---------------------------------------------------------
    # request
    # ---------------------------------------------------------

    def _apply_session_cookies(
        self,
        context: RequestContext,
    ) -> None:

        session = self._get_session(context)

        if session is None:
            return

        session_cookies = session.cookies

        if not session_cookies:
            return

        context.descriptor = (
            RequestBuilder
            .from_descriptor(
                context.descriptor,
            )
            .merge_cookies(
                session_cookies,
                override=False,
            )
            .build()
        )
    # ---------------------------------------------------------
    # response
    # ---------------------------------------------------------

    def _update_session_cookies(
        self,
        context: RequestContext,
    ) -> None:

        session = self._get_session(
            context,
        )

        if session is None:
            return

        result = context.result

        if result is None:
            return

        if not result.success:
            return

        response = result.response

        if response is None:
            return

        cookies = response.cookies

        if not cookies:
            return

        session.cookies.update(
            cookies,
        )

    # ---------------------------------------------------------
    # session
    # ---------------------------------------------------------

    def _get_session(
        self,
        context: RequestContext,
    ) -> Session | None:

        return context.runtime.get(
            SESSION_RUNTIME_KEY,
        )