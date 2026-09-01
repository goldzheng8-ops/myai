from __future__ import annotations

from core.request.context import RequestContext
from core.request.middleware.base import RequestMiddleware
from core.request.middleware.config import SessionMiddlewareConfig
from core.request.middleware.typing import MiddlewareType, RequestMiddlewareNext

from .model import Session
from .store import SessionStore


SESSION_RUNTIME_KEY = "request.session"


class SessionMiddleware(RequestMiddleware[SessionMiddlewareConfig]):
    plugin_type = MiddlewareType.SESSION
    def __init__(
        self,
        store: SessionStore,
        config: SessionMiddlewareConfig,
    ) -> None:
        super().__init__(
            config
        )
        self._store = store

    @property
    def store(self) -> SessionStore:
        return self._store
    @property
    def config(self) -> SessionMiddlewareConfig:
        return self._config
    
    async def process(
        self,
        context: RequestContext,
        next_: RequestMiddlewareNext,
    ) -> RequestContext:

        session_id = self._resolve_session_id(
            context,
        )

        if session_id is None:
            return await next_(context)

        context.session_id = session_id

        session = await self._store.get(
            session_id,
        )

        if session is None:

            if not self.config.create_if_missing:
                return await next_(context)

            session = Session(
                id=session_id,
            )

        context.runtime.set(
            SESSION_RUNTIME_KEY,
            session,
        )

        try:

            return await next_(
                context,
            )

        finally:

            if self.config.save_after_request:
                await self._store.save(
                    session,
                )

    def _resolve_session_id(
        self,
        context: RequestContext,
    ) -> str | None:

        if context.session_id is not None:
            return context.session_id

        return self.config.default_session_id