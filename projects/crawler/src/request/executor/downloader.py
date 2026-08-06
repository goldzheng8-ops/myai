from core.request_pipeline.executor import PipelineExecutor
from models.runtime.request.pipeline import RequestPipelineContext






class DownloaderPipelineExecutor(
    PipelineExecutor[RequestPipelineContext],
):

    def __init__(
        self,
        downloader: DownloaderExecutor,
    ) -> None:

        self._downloader = downloader

    async def execute(
        self,
        context: RequestPipelineContext,
    ) -> RequestPipelineContext:

        try:

            context.response = await self._downloader.download(
                context.request,
            )

        except Exception as exc:

            context.exception = exc

        return context