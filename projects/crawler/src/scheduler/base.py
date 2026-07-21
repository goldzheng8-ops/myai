from abc import ABC, abstractmethod
from collections.abc import AsyncIterator


class BaseScheduler(ABC):

    @abstractmethod
    async def events(
        self,
    ) -> AsyncIterator[ScheduleEvent]:
        ...