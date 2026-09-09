from __future__ import annotations


from .protocol import LifecycleParticipant


class LifecycleManager:

    def __init__(self) -> None:
        self._participants: list[
            LifecycleParticipant
        ] = []

        self._registered: set[int] = set()
        self._started: set[int] = set()

        self._closed = False

    def register(
        self,
        participant: LifecycleParticipant,
    ) -> LifecycleParticipant:
        """
        Register a lifecycle participant.

        Registration does not start the participant.
        The participant will be started by ``start()``.
        """

        if self._closed:
            raise RuntimeError(
                "Cannot register a participant after "
                "the lifecycle manager has been closed."
            )

        identity = id(participant)

        if identity not in self._registered:
            self._participants.append(participant)
            self._registered.add(identity)

        return participant

    async def acquire(
        self,
        participant: LifecycleParticipant,
    ) -> LifecycleParticipant:
        """
        Acquire and immediately start a lifecycle participant.

        This method is kept for backward compatibility with the
        previous lazy-loading lifecycle model.
        """

        if self._closed:
            raise RuntimeError(
                "Cannot acquire a participant after "
                "the lifecycle manager has been closed."
            )

        identity = id(participant)

        # Already registered and started.
        if identity in self._started:
            return participant

        # Register first so that the participant becomes part of
        # the lifecycle even when it is acquired dynamically.
        self.register(participant)

        try:
            await participant.start()
        except Exception:
            # Registration succeeded, but startup failed.
            #
            # Keep the participant registered so that lifecycle
            # ownership remains explicit, but do not mark it
            # as started.
            raise

        self._started.add(identity)

        return participant

    async def start(self) -> None:
        """
        Start all registered participants.

        Participants are started in registration order.
        If startup fails, already-started participants are closed
        in reverse order.
        """

        if self._closed:
            raise RuntimeError(
                "Cannot start a closed lifecycle manager."
            )

        started: list[LifecycleParticipant] = []

        try:
            for participant in self._participants:
                identity = id(participant)

                if identity in self._started:
                    continue

                await participant.start()

                self._started.add(identity)
                started.append(participant)

        except Exception:
            for participant in reversed(started):
                try:
                    await participant.close()
                except Exception:
                    logger.exception(
                        "Failed to close lifecycle "
                        "participant after startup failure: %r",
                        participant,
                    )

            for participant in started:
                self._started.discard(id(participant))

            raise

    async def close(self) -> None:
        """
        Close all started participants in reverse order.

        Close is idempotent.
        """

        if self._closed:
            return

        self._closed = True

        for participant in reversed(self._participants):
            identity = id(participant)

            if identity not in self._started:
                continue

            try:
                await participant.close()
            except Exception:
                logger.exception(
                    "Failed to close lifecycle "
                    "participant: %r",
                    participant,
                )

        self._participants.clear()
        self._registered.clear()
        self._started.clear()

    @property
    def closed(self) -> bool:
        return self._closed

    @property
    def participants(
        self,
    ) -> tuple[LifecycleParticipant, ...]:
        return tuple(self._participants)