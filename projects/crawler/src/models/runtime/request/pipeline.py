from dataclasses import dataclass

from core.request_pipeline.context import PipelineContext
from core.request.downloader.result import DownloadResult


from ....core.request.context import RequestContext


@dataclass(slots=True)
class RequestPipelineContext(PipelineContext):
    """
    HTTP 请求 Pipeline 的上下文。

    整个 Request Pipeline 在生命周期内共享此对象。
    """

    request: RequestContext

    response: DownloadResult | None = None

    exception: Exception | None = None

    aborted: bool = False