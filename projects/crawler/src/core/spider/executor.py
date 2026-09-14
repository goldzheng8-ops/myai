from __future__ import annotations

from collections import deque
from dataclasses import dataclass
from typing import Sequence
from application.config.registry import SpiderConfigRegistry
from core.extraction.extractor.context import ExtractContext
from core.request.context import RequestContext
from core.request.descriptor import RequestDescriptor
from core.runtime import RuntimeContext
from core.spider.registry import SpiderRegistry


from .context import SpiderContext
from .result import SpiderResult
from .services import SpiderServices




@dataclass(frozen=True, slots=True)
class SpiderRequest:
    """
    Scheduled spider request.

    Keeps the descriptor and its already-computed fingerprint
    together so that fingerprint calculation is not repeated
    during request execution.
    """

    descriptor: RequestDescriptor

    fingerprint: str

class SpiderExecutor:
    """
    Executes the request/discovery/extraction lifecycle
    of a spider.
    """

    def __init__(
        self,
        services: SpiderServices,
        spider_registry: SpiderRegistry,
        spider_config_registry: SpiderConfigRegistry,
        runtime: RuntimeContext
    ) -> None:

        self._services = services
        self._spider_registry=spider_registry
        self._spider_config_registry=spider_config_registry
        self._runtime=runtime

    @property
    def services(
        self,
    ) -> SpiderServices:

        return self._services

    async def execute(
        self,
        descriptors:Sequence[RequestDescriptor]
    ) -> SpiderResult:

        result = SpiderResult()

        queue: deque[SpiderRequest] = deque()

        seen: set[str] = set()

        for descriptor in descriptors:
            if self._enqueue(
                descriptor,
                queue,
                seen,
            ):
                result.request_count += 1

        while queue:

            item = queue.popleft()
            descriptor=item.descriptor
            # if descriptor.target_spider is None:
            #     raise ConfigurationError(
            #         "Request descriptor has no target spider."
            #     )
            spider_config=self._spider_config_registry.get(descriptor.target_spider)
            spider_context  = SpiderContext(
                config=spider_config,
                runtime=self._runtime,
            )
            spider=self._spider_registry.create(spider_config.template)
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
                continue
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
                print(queue.__len__())

                await extract_context.response.close()

            if step.item is not None:
                await self._services.output_engine.write(
                    step.item,
                    step.outputs,
                )
                result.item_count += 1

            for descriptor in step.requests:
                if self._enqueue(
                    descriptor,
                    queue,
                    seen,
                ):
                    result.request_count += 1

            if not step.continue_:
                break

            spider_context.result = result

        return result

    def _enqueue(
        self,
        descriptor: RequestDescriptor,
        queue: deque[SpiderRequest],
        seen: set[str],
    ) -> bool:

        fingerprint = (
            self._services.fingerprint_provider.fingerprint(
                descriptor,
            )
        )

        if not descriptor.meta.dont_filter:

            if fingerprint in seen:
                return False

            seen.add(
                fingerprint,
            )

        queue.append(
            SpiderRequest(
                descriptor=descriptor,
                fingerprint=fingerprint,
            ),
        )

        return True

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
