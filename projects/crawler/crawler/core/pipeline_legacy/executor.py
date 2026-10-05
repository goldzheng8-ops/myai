from __future__ import annotations

from core.pipeline_legacy.protocol import PipelineExecutorProtocol

from .pipeline import Pipeline
from .pipeline_runner import PipelineRunner
from .runtime import PipelineRuntime
from .stage_runner import StageRunner
from .pass_runner import PassRunner
from .typing import ContextT


class PipelineExecutor(
    PipelineExecutorProtocol[ContextT],
):

    def __init__(
        self,
        runner: PipelineRunner[ContextT] | None = None,
    ) -> None:

        if runner is None:

            runner = PipelineRunner(
                StageRunner(
                    PassRunner(),
                ),
            )

        self._runner = runner

    @property
    def runner(
        self,
    ) -> PipelineRunner[
        ContextT
    ]:

        return self._runner

    async def execute(
        self,
        pipeline: Pipeline[ContextT],
        context: ContextT,
    ) -> ContextT:

        runtime = PipelineRuntime.create(
            pipeline,
        )

        return await self._runner.run(
            context,
            runtime,
        )