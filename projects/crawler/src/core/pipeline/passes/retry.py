

from core.pipeline.pass_ import PipelinePass
from core.pipeline.runtime import PipelineRuntime
from core.pipeline.typing import ContextT,PipelineNext


class RetryPass(PipelinePass[ContextT]):

    def __init__(
        self,
        retries: int = 3,
        delay: float = 0,
        exceptions: tuple[type[Exception], ...] = (Exception,),
        **kwargs,
    ):

        super().__init__(**kwargs)

        self._retries = retries

        self._delay = delay

        self._exceptions = exceptions

    async def process(
        self,
        context: ContextT,
        runtime: PipelineRuntime,
        next_step: PipelineNext[ContextT],
    ):

        import asyncio

        attempt = 0

        while True:
            runtime.metadata.setdefault(
                "retry",
                {},
            )["attempt"] = attempt

            try:

                return await next_step(
                    context,
                    runtime,
                )

            except self._exceptions:

                attempt += 1


                if attempt > self._retries:
                    raise

                if self._delay:

                    await asyncio.sleep(
                        self._delay
                    )