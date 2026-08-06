from core.request_pipeline.pipeline import DefaultPipeline
from models.runtime.extract.context import RequestContext
from models.runtime.request.pipeline import RequestPipelineContext




class RequestEngine:

    def __init__(
        self,
        pipeline: DefaultPipeline[
            RequestPipelineContext,
        ],
    ) -> None:

        self._pipeline = pipeline

    async def execute(
        self,
        context: RequestContext,
    ) -> RequestPipelineContext:

        return await self._pipeline.execute(
            RequestPipelineContext(
                request=context,
            )
        )