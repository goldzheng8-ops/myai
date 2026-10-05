from typing import Generic
from .typing import ContextT
from .runtime import PipelineRuntime


class PassRunner(
    Generic[ContextT],
):

    async def run(
        self,
        context: ContextT,
        runtime: PipelineRuntime,
    ) -> ContextT:

        assert runtime.step is not None

        next_step = self._terminal

        for current in reversed(runtime.step):

            previous = next_step

            async def middleware(
                ctx: ContextT,
                rt: PipelineRuntime,
                current=current,
                nxt=previous,
            ):

                rt.pass_ = current

                return await current.process(
                    ctx,
                    rt,
                    nxt,
                )

            next_step = middleware

        return await next_step(
            context,
            runtime,
        )

    async def _terminal(
        self,
        context: ContextT,
        runtime: PipelineRuntime,
    ) -> ContextT:

        return context