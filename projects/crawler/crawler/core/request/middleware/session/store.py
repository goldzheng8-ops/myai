from __future__ import annotations
import asyncio
from typing import Protocol

from .model import Session


class SessionStore(Protocol):

    async def get(
        self,
        session_id: str,
    ) -> Session | None:
        ...

    async def save(
        self,
        session: Session,
    ) -> None:
        ...

class MemorySessionStore:

    def __init__(self) -> None:

        self._sessions: dict[
            str,
            Session,
        ] = {}

        self._lock = asyncio.Lock()

    async def get(
        self,
        session_id: str,
    ) -> Session | None:

        async with self._lock:

            session = self._sessions.get(
                session_id,
            )

            return session

    async def save(
        self,
        session: Session,
    ) -> None:

        async with self._lock:

            self._sessions[
                session.id
            ] = session