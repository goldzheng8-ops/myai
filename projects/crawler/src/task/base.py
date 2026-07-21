from abc import ABC, abstractmethod
from collections.abc import AsyncIterator

from task.model import Task


class TaskProvider(ABC):

    @abstractmethod
    async def tasks(
        self
    ) -> AsyncIterator[Task]:
        ...