from typing import Generic
from .typing import ContextT
from .pass_runner import PassRunner
from .runtime import PipelineRuntime


class StageRunner(
    Generic[ContextT],
):

    def __init__(
        self,
        pass_runner: PassRunner[
            ContextT
        ],
    ):

        self._pass_runner = pass_runner

    async def run(
        self,
        context: ContextT,
        runtime: PipelineRuntime,
    ) -> ContextT:

        assert runtime.stage is not None

        for step in runtime.stage:

            runtime.step = step

            context = await self._pass_runner.run(
                context,
                runtime,
            )

            if runtime.cancelled:
                break

        return context