from __future__ import annotations

from abc import ABC, abstractmethod

from ..context import RequestContext


class RequestExecutor(ABC):
    """
    Terminal executor for a request.

    Concrete implementations perform the actual I/O operation.
    """

    @abstractmethod
    async def execute(
        self,
        context: RequestContext,
    ) -> RequestContext:
        """
        Execute the actual request and update its context.
        """

        raise NotImplementedError

class DownloaderRequestExecutor(
    RequestExecutor,
):

    def __init__(
        self,
        downloader: Downloader,
    ) -> None:

        self._downloader = downloader

    async def execute(
        self,
        context: RequestContext,
    ) -> RequestContext:

        result = await self._downloader.download(
            context.descriptor,
        )

        context.result = result

        return context