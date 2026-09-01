import pprint

from core.pipeline_legacy.runtime import PipelineRuntime

from .monitoring import MonitoringPass
from core.pipeline_legacy.typing import ContextT

class DebugPass(
    MonitoringPass[ContextT],
):

    async def before(
        self,
        context: ContextT,
        runtime: PipelineRuntime,
    ):

        pprint.pp({

            "pipeline": runtime.pipeline.name,

            "stage": runtime.stage.name,

            "step": runtime.step.name,

            "pass": runtime.pass_.name,

            "metadata": runtime.metadata,

            "context": context.as_mapping(),

        })