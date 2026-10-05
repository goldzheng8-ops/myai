from typing import AsyncIterator, Protocol

from core.request.context import RequestContext


class StreamingDownloader(
    Protocol,
):
    async def stream(
        self,
        context: RequestContext,
    ) -> AsyncIterator[bytes]:
        ...