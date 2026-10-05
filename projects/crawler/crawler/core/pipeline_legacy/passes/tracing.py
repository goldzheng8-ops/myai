from dataclasses import dataclass

from core.pipeline_legacy.runtime import PipelineRuntime
from core.pipeline_legacy.typing import ContextT
from .monitoring import MonitoringPass


@dataclass(slots=True)
class TraceRecord:

    pipeline: str

    stage: str

    step: str

    pass_name: str




class TracingPass(
    MonitoringPass[ContextT],
):

    async def before(
        self,
        context: ContextT,
        runtime: PipelineRuntime,
    ):

        runtime.metadata.setdefault(
            "trace",
            [],
        ).append(

            TraceRecord(
                pipeline=runtime.pipeline.name,
                stage=runtime.stage.name,
                step=runtime.step.name,
                pass_name=runtime.pass_.name,
            )

        )