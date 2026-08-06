import time

from core.pipeline.runtime import PipelineRuntime
from core.pipeline.typing import ContextT

from .monitoring import MonitoringPass


class MetricsPass(
    MonitoringPass[ContextT],
):

    async def before(
        self,
        context: ContextT,
        runtime: PipelineRuntime,
    ):

        runtime.metadata.setdefault(
            "metrics",
            {},
        )["start"] = time.perf_counter()

    async def after(
        self,
        context: ContextT,
        runtime: PipelineRuntime,
    ):

        metrics = runtime.metadata["metrics"]

        metrics["elapsed"] = (
            time.perf_counter()
            - metrics["start"]
        )