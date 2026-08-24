from __future__ import annotations

from core.request.context import RequestContext
from core.request.middleware.base import RequestMiddleware
from core.request.middleware.config import MiddlewareConfig
from core.request.middleware.typing import RequestMiddlewareNext

from .model import Session
from .policy import SessionPolicy
from .store import SessionStore


SESSION_RUNTIME_KEY = "request.session"


class SessionMiddleware(RequestMiddleware):

    def __init__(
        self,
        store: SessionStore,
        policy: SessionPolicy,
        config: MiddlewareConfig | None = None,
    ) -> None:
        super().__init__(
            config
            if config is not None
            else MiddlewareConfig(),
        )
        self._store = store

        self._policy =policy

    @property
    def store(self) -> SessionStore:
        return self._store

    @property
    def policy(self) -> SessionPolicy:
        return self._policy

    async def process(
        self,
        context: RequestContext,
        next_: RequestMiddlewareNext,
    ) -> RequestContext:

        if not self._policy.enabled:
            return await next_(context)

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

            if not self._policy.create_if_missing:
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

            if self._policy.save_after_request:
                await self._store.save(
                    session,
                )

    def _resolve_session_id(
        self,
        context: RequestContext,
    ) -> str | None:

        if context.session_id is not None:
            return context.session_id

        return self._policy.default_session_id