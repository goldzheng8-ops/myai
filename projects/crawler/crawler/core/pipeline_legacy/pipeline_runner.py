from typing import Generic
from .typing import ContextT
from .stage_runner import StageRunner
from .runtime import PipelineRuntime

class PipelineRunner(
    Generic[ContextT],
):

    def __init__(
        self,
        stage_runner: StageRunner[
            ContextT
        ],
    ):

        self._stage_runner = stage_runner

    async def run(
        self,
        context: ContextT,
        runtime: PipelineRuntime,
    ) -> ContextT:

        for stage in runtime.pipeline:

            runtime.stage = stage

            context = await self._stage_runner.run(
                context,
                runtime,
            )

            if runtime.cancelled:
                break

        return context