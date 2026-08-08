# core/event/dispatcher.py

from __future__ import annotations

import asyncio
from typing import Generic, Protocol, Sequence

from core.runtime.merge import ContextMergeStrategy

from .event import Event
from .handler import EventHandlerRegistration
from .policy import EventDispatchPolicy
from .provider import EventHandlerProvider
from .typing import ContextT, DispatchMode

class EventDispatcherProtocol(Protocol[ContextT]):

    async def dispatch(
        self,
        event: Event,
        context: ContextT,
    ) -> ContextT:
        ...
        
class EventDispatcher(
    EventDispatcherProtocol[ContextT],
    Generic[ContextT],
):
    """
    Dispatch events to registered handlers.

    The dispatcher is responsible only for:

    - obtaining handlers from the provider;
    - selecting the execution mode;
    - executing handlers;
    - merging parallel results.

    It does not know how handlers are registered.
    """

    def __init__(
        self,
        provider: EventHandlerProvider[ContextT],
        policy: EventDispatchPolicy | None = None,
        merge_strategy: ContextMergeStrategy | None = None,
    ) -> None:

        self._provider = provider

        self._policy = (
            policy
            if policy is not None
            else EventDispatchPolicy()
        )

        self._merge_strategy = merge_strategy

        if (
            self._policy.mode is DispatchMode.PARALLEL
            and self._merge_strategy is None
        ):
            raise ValueError(
                "Parallel event dispatch requires "
                "a ContextMergeStrategy."
            )

    @property
    def provider(
        self,
    ) -> EventHandlerProvider[ContextT]:

        return self._provider

    @property
    def policy(
        self,
    ) -> EventDispatchPolicy:

        return self._policy

    @property
    def merge_strategy(
        self,
    ) -> ContextMergeStrategy | None:

        return self._merge_strategy

    async def dispatch(
        self,
        event: Event,
        context: ContextT,
    ) -> ContextT:

        registrations = self._provider.provide(
            event,
        )

        if not registrations:
            return context

        if (
            self._policy.mode
            is DispatchMode.SEQUENTIAL
        ):
            return await self._dispatch_sequential(
                event,
                context,
                registrations,
            )

        return await self._dispatch_parallel(
            event,
            context,
            registrations,
        )

    async def _dispatch_sequential(
        self,
        event: Event,
        context: ContextT,
        registrations: Sequence[
            EventHandlerRegistration[ContextT]
        ],
    ) -> ContextT:

        current = context

        for registration in registrations:

            try:

                current = await (
                    registration.handler.handle(
                        event,
                        current,
                    )
                )

            except Exception:

                if self._policy.stop_on_error:
                    raise

                continue

        return current

    async def _dispatch_parallel(
        self,
        event: Event,
        context: ContextT,
        registrations: Sequence[
            EventHandlerRegistration[ContextT]
        ],
    ) -> ContextT:

        tasks = [
            self._execute_parallel_handler(
                event,
                context,
                registration,
            )
            for registration in registrations
        ]

        results = await asyncio.gather(
            *tasks,
            return_exceptions=True,
        )

        successful: list[ContextT] = []

        first_exception: BaseException | None = None

        for result in results:

            if isinstance(
                result,
                BaseException,
            ):

                if first_exception is None:
                    first_exception = result

                continue

            successful.append(result)

        if (
            first_exception is not None
            and self._policy.stop_on_error
        ):
            raise first_exception

        if self._merge_strategy is None:
            raise RuntimeError(
                "Parallel dispatch requires "
                "a ContextMergeStrategy."
            )

        for result in successful:

            self._merge_strategy.merge(
                context,
                result,
            )

        return context

    async def _execute_parallel_handler(
        self,
        event: Event,
        context: ContextT,
        registration: EventHandlerRegistration[ContextT],
    ) -> ContextT:

        handler_context = context.copy()

        return await registration.handler.handle(
            event,
            handler_context,
        )