

from task.base import TaskProvider


r


class CronScheduler:
    def __init__(self, task_provider: "TaskProvider"):
        self.task_provider = task_provider

    async def run(self) -> None:
        async for task in self.task_provider.list_tasks():
            await task.execute()