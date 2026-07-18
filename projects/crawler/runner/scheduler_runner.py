class SchedulerRunner:

    def __init__(
        self,

        scheduler,

        provider,

        factory,

        runner,
    ):
        self.scheduler = scheduler

        self.provider = provider

        self.factory = factory

        self.runner = runner

    async def run(self):

        async for event in self.scheduler.events():

            async for task in self.provider.tasks():

                context = self.factory.create(task)

                await self.runner.run(context)