from __future__ import annotations

from collections import deque
from dataclasses import dataclass
from typing import Generic

from core.request.builder import RequestBuilder
from core.request.context import RequestContext
from core.request.descriptor import RequestDescriptor


from .context import SpiderContext
from .result import SpiderResult
from .services import SpiderServices
from .template.base import TemplateSpider
from .typing import ConfigT


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


class SpiderExecutor(Generic[ConfigT]):
    """
    Executes the request/discovery/extraction lifecycle
    of a spider.
    """

    def __init__(
        self,
        services: SpiderServices,
    ) -> None:

        self._services = services

    @property
    def services(
        self,
    ) -> SpiderServices:

        return self._services

    async def execute(
        self,
        spider: TemplateSpider[ConfigT],
        context: SpiderContext[ConfigT],
    ) -> SpiderResult:

        result = SpiderResult()

        queue: deque[SpiderRequest] = deque()

        seen: set[str] = set()

        for request in context.config.start_requests:

            descriptor = RequestBuilder.from_request(
                request,
                kind=context.config.kind,
                profile=context.config.profile,
            )

            self._enqueue(
                descriptor,
                queue,
                seen,
            )

        while queue:

            item = queue.popleft()

            request_context = RequestContext(
                descriptor=item.descriptor,
                runtime=context.runtime,
                fingerprint=item.fingerprint,
            )

            request_context = (
                await self._services.request_runner.run(
                    request_context,
                )
            )

            step = await spider.process(
                context,
                request_context,
            )

            result.items.extend(
                step.items,
            )

            result.requests.extend(
                step.requests,
            )

            for descriptor in step.requests:

                self._enqueue(
                    descriptor,
                    queue,
                    seen,
                )

            if not step.continue_:
                break

        context.result = result

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