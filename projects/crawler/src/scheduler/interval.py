class IntervalScheduler(BaseScheduler):

    def __init__(
        self,
        seconds: int,
    ):
        self.seconds = seconds


    async def events(self):

        while True:

            yield ScheduleEvent(
                time=datetime.now()
            )

            await asyncio.sleep(
                self.seconds
            )