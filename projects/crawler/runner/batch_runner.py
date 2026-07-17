

class BatchRunner:


    async def run(
        self,
        provider: TaskProvider
    ):

        async for task in provider.tasks():

            context = self.factory.create(task)

            result = await self.single_runner.run(
                context
            )

            yield result