from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import ClassVar

from application.config.registry import SpiderConfigRegistry
from core.output.model import DownloadResult, OutputItem
from core.request.context import RequestContext
from core.request.descriptor import RequestDescriptor
from core.request.typing import RequestKind
from core.runtime import RuntimeContext
from core.spider.config import SpiderConfig
from core.spider.context import SpiderContext
from core.spider.registry import SpiderRegistry
from core.spider.services import SpiderServices
from core.spider.step import RequestStep
from core.spider.template.extraction import RequestTemplate


@dataclass(slots=True)
class TemplateExecutionContext:
    spider: SpiderContext[SpiderConfig]
    request: RequestContext
    template: RequestTemplate[SpiderConfig]

@dataclass(slots=True)
class RequestExecutionResult:
    item: OutputItem | None = None
    download: DownloadResult | None = None

    outputs: tuple[str, ...] = ()

    requests: list[RequestDescriptor] = field(
        default_factory=list,
    )

    continue_: bool = True

@dataclass(frozen=True, slots=True)
class ScheduledRequest:
    """
    Scheduled spider request.

    Keeps the descriptor and its already-computed fingerprint
    together so that fingerprint calculation is not repeated
    during request execution.
    """

    descriptor: RequestDescriptor

    fingerprint: str

class RequestKindHandler(ABC):

    # Provide a default class-level value so type checkers (Pylance)
    # can reliably see the attribute on instances and subclasses.
    kinds: ClassVar[frozenset[RequestKind]] = frozenset()
    @abstractmethod
    async def execute(
        self,
        item: ScheduledRequest,
    ) -> RequestExecutionResult:
        ...

class TemplateRequestHandler(
    RequestKindHandler,
    ABC,
):
    """
    Executes requests through a configured RequestTemplate.
    """

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

        execution = await self._prepare(item)

        request = execution.request

        if request.state.is_skipped:
            return RequestExecutionResult()

        try:
            step = await execution.template.process(
                context=execution.spider,
                request=request,
            )

            return self._build_execution_result(step)

        finally:
            await self._close_response(request)

    async def _prepare(
        self,
        item: ScheduledRequest,
    ) -> TemplateExecutionContext:

        descriptor = item.descriptor

        spider_config = (
            self._spider_config_registry.get(
                descriptor.target_spider,
            )
        )

        spider_context = SpiderContext(
            config=spider_config,
            runtime=self._runtime,
        )

        template = self._spider_registry.create(
            spider_config.template,
        )

        request_context = RequestContext(
            configs=spider_config.middlewares,
            descriptor=descriptor,
            runtime=spider_context.runtime,
            fingerprint=item.fingerprint,
        )

        request_context = (
            await self._services.request_runner.run(
                request_context,
            )
        )

        return TemplateExecutionContext(
            spider=spider_context,
            request=request_context,
            template=template,
        )

    @staticmethod
    async def _close_response(
        context: RequestContext,
    ) -> None:

        if context.result is None:
            return

        await context.result.response.close()

    @staticmethod
    def _build_execution_result(
        step: RequestStep,
    ) -> RequestExecutionResult:

        return RequestExecutionResult(
            item=step.item,
            download=step.download,
            outputs=step.outputs,
            requests=step.requests,
            continue_=step.continue_,
        )