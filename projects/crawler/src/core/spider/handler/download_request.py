from core.request.context import RequestContext
from core.request.typing import RequestKind
from core.runtime import RuntimeContext
from core.spider.handler.base import RequestExecutionResult, RequestKindHandler, ScheduledRequest
from core.spider.services import SpiderServices


class DownloadRequestHandler(RequestKindHandler):
    kinds = frozenset({
        RequestKind.DOWNLOAD,
    })

    def __init__(
        self,
        services: SpiderServices,
        runtime: RuntimeContext,
    ) -> None:
        self._services = services
        self._runtime = runtime

    async def execute(
        self,
        item: ScheduledRequest,
    ) -> RequestExecutionResult:

        descriptor = item.descriptor

        request_context = RequestContext(
            configs=(),
            descriptor=descriptor,
            runtime=self._runtime,
            fingerprint=item.fingerprint,
        )

        request_context = (
            await self._services.request_runner.run(
                request_context,
            )
        )

        if request_context.state.is_skipped:
            return RequestExecutionResult()

        result = request_context.result

        if result is None:
            raise RuntimeError(
                "Download request produced no result.",
            )

        response = result.response

        if response is None:
            raise RuntimeError(
                "Download request produced no response.",
            )

        # download = DownloadResult(
        #     url=response.url,
        #     body=response.body,
        #     content_type=(
        #         response.headers.get("content-type")
        #     ),
        # )

        # 第一阶段先不决定具体保存方式。
        # 后面交给 DownloadOutput / FileOutputSink。

        return RequestExecutionResult()