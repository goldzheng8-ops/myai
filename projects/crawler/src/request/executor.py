from core.request_pipeline.executor import PipelineExecutor
from models.runtime.request.pipeline import RequestPipelineContext

class RequestExecutor(
    PipelineExecutor[RequestPipelineContext]
):
    ...