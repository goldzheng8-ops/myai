# core/event/registry.py

from __future__ import annotations

from core.registry.multi import MultiRegistry

from .handler import EventHandlerRegistration
from .typing import ContextT, EventKey


class EventRegistry(
    MultiRegistry[
        EventKey,
        EventHandlerRegistration[ContextT],
    ],
):
    """
    Registry of event handlers.

    One EventKey may have multiple registered handlers.
    """

    def register_handler(
        self,
        key: EventKey,
        registration: EventHandlerRegistration[ContextT],
    ) -> None:

        self.add(
            key,
            registration,
        )

    def unregister_handler(
        self,
        key: EventKey,
        registration: EventHandlerRegistration[ContextT],
    ) -> None:

        return self.remove(
            key,
            registration,
        )