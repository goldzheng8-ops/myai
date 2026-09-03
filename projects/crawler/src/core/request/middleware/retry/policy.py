from typing import Protocol

from core.request.context import RequestContext


class RetryPolicy(Protocol):

    def should_retry(
        self,
        *,
        context: RequestContext,
        exception: BaseException,
    ) -> bool:
        ...