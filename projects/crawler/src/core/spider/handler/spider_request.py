from application.config.registry import SpiderConfigRegistry
# from core.exception.application import ConfigurationError
from core.extraction.extractor.context import ExtractContext
from core.request.context import RequestContext
from core.request.typing import RequestKind
from core.runtime import RuntimeContext
from core.spider.context import SpiderContext
from core.spider.handler.base import RequestExecutionResult, RequestKindHandler, ScheduledRequest
from core.spider.registry import SpiderRegistry
from core.spider.services import SpiderServices


class SpiderRequestHandler(RequestKindHandler):
    kinds = frozenset({
        RequestKind.LIST,
        RequestKind.DETAIL,
        RequestKind.API,
    })

    def __init__(
        self,
        services: SpiderServices,
        spider_registry: SpiderRegistry,
        spider_config_registry: SpiderConfigRegistry,
        runtime: RuntimeContext,
    ) -> None:
        self._services = services
        self._spider_registry = spider_registry
        self._spider_config_registry = (
            spider_config_registry
        )
        self._runtime = runtime

    async def execute(
        self,
        item: ScheduledRequest,
    ) -> RequestExecutionResult:

        descriptor = item.descriptor

        # if descriptor.target_spider is None:
        #     raise ConfigurationError(
        #         "Spider request has no target spider.",
        #     )

        spider_config = (
            self._spider_config_registry.get(
                descriptor.target_spider,
            )
        )

        spider_context = SpiderContext(
            config=spider_config,
            runtime=self._runtime,
        )

        spider = self._spider_registry.create(
            spider_config.template,
        )

        request_context = RequestContext(
            configs=spider_context.config.middlewares,
            descriptor=descriptor,
            runtime=spider_context.runtime,
            fingerprint=item.fingerprint,
        )

        request_context = (
            await self._services.request_runner.run(
                request_context,
            )
        )

        if request_context.state.is_skipped:
            return RequestExecutionResult()

        extract_context = (
            self._build_extract_context(
                request_context,
            )
        )

        try:
            step = await spider.process(
                spider_context,
                request_context,
                extract_context,
            )
        finally:
            await extract_context.response.close()

        return RequestExecutionResult(
            item=step.item,
            outputs=step.outputs,
            requests=step.requests,
            continue_=step.continue_,
        )

    def _build_extract_context(
        self,
        request_context: RequestContext,
    ) -> ExtractContext:

        result = request_context.result

        if result is None:
            raise RuntimeError(
                "Request execution produced no result.",
            )

        response = result.response

        if response is None:
            raise RuntimeError(
                "Request execution produced no response.",
            )

        adapter = (
            self._services
            .response_adapter_resolver
            .resolve(
                profile=request_context.descriptor.profile,
                response=response,
            )
        )

        return ExtractContext(
            request=request_context,
            response=adapter,
            runtime=request_context.runtime,
        )