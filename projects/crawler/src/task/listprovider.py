from collections.abc import AsyncIterator

from task.base import TaskProvider
from task.model import Task


class ListTaskProvider(TaskProvider):

    def __init__(
        self,
        tasks:list[Task]
    ):
        self._tasks = tasks


    async def tasks(
        self
    ) -> AsyncIterator[Task]:

        for task in self._tasks:
            yield task