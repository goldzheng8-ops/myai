# core/event/provider.py

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Generic, Sequence

from .event import Event
from .handler import EventHandlerRegistration
from .registry import EventRegistry
from .typing import ContextT


class EventHandlerProvider(
    ABC,
    Generic[ContextT],
):
    """
    Provides event handler registrations for an Event.
    """

    @abstractmethod
    def provide(
        self,
        event: Event,
    ) -> Sequence[
        EventHandlerRegistration[ContextT]
    ]:
        ...


class RegistryEventHandlerProvider(
    EventHandlerProvider[ContextT],
):
    """
    EventHandlerProvider backed by EventRegistry.
    """

    def __init__(
        self,
        registry: EventRegistry[ContextT],
    ) -> None:

        self._registry = registry

    @property
    def registry(
        self,
    ) -> EventRegistry[ContextT]:

        return self._registry

    def provide(
        self,
        event: Event,
    ) -> tuple[
        EventHandlerRegistration[ContextT],
        ...,
    ]:

        registrations = self._registry.get_all(
            event.key,
        )

        enabled = (
            registration
            for registration in registrations
            if registration.enabled
        )

        return tuple(
            sorted(
                enabled,
                key=lambda registration: registration.priority,
                reverse=True,
            )
        )