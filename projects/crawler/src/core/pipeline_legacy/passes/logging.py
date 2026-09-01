import logging
import time

from core.pipeline_legacy.runtime import PipelineRuntime

from .monitoring import MonitoringPass
from core.pipeline_legacy.typing import ContextT

class LoggingPass(
    MonitoringPass[ContextT],
):

    def __init__(
        self,
        logger: logging.Logger | None = None,
        **kwargs,
    ):

        super().__init__(**kwargs)

        self._logger = logger or logging.getLogger(__name__)

        self._start = 0.0

    async def before(
        self,
        context: ContextT,
        runtime: PipelineRuntime,
    ):

        self._start = time.perf_counter()

        self._logger.info(
            "Pipeline=%s Stage=%s Step=%s Pass=%s Started",
            runtime.pipeline.name,
            runtime.stage.name if runtime.stage else "",
            runtime.step.name if runtime.step else "",
            runtime.pass_.name if runtime.pass_ else "",
        )

    async def after(
        self,
        context: ContextT,
        runtime: PipelineRuntime,
    ):

        elapsed = time.perf_counter() - self._start

        self._logger.info(
            "Pipeline=%s Finished %.3fs",
            runtime.pipeline.name,
            elapsed,
        )