from __future__ import annotations


from .protocol import LifecycleParticipant


class LifecycleManager:
    """
    Manage the lifecycle of runtime participants.

    Participants are started when acquired and closed in reverse
    acquisition order.
    """

    def __init__(self) -> None:
        self._participants: list[LifecycleParticipant] = []
        self._started: set[int] = set()
        self._closed = False

    async def acquire(
        self,
        participant: LifecycleParticipant,
    ) -> LifecycleParticipant:
        """
        Start and track a lifecycle participant.

        A participant is started at most once for this manager.
        """

        if self._closed:
            raise RuntimeError(
                "Cannot acquire a participant after "
                "the lifecycle manager has been closed."
            )

        identity = id(participant)

        if identity in self._started:
            return participant


        await participant.start()


        self._participants.append(participant)
        self._started.add(identity)

        return participant

    async def close(self) -> None:
        """
        Close all acquired participants in reverse order.

        Close is idempotent.
        """

        if self._closed:
            return

        self._closed = True

        for participant in reversed(self._participants):
            await participant.close()

        self._participants.clear()
        self._started.clear()

    @property
    def closed(self) -> bool:
        return self._closed

    @property
    def participants(
        self,
    ) -> tuple[LifecycleParticipant, ...]:
        return tuple(self._participants)