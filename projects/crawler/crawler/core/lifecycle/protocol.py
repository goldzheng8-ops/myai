from typing import Protocol


class LifecycleParticipant(Protocol):
    async def start(self) -> None:
        ...

    async def close(self) -> None:
        ...