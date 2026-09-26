from __future__ import annotations

from typing import Generic

from core.extraction.response.resolver import ResponseAdapterResolver
from core.request.context import RequestContext
from core.request.downloader.model import DownloaderCapabilities
from core.request.response.model import RequestResponse



from .plugin import DownloadResult, DownloaderPlugin
from .request import DownloadRequest

from .typing import ConfigT




class BaseDownloader(
    DownloaderPlugin,
    Generic[ConfigT],
):
    """
    Base implementation shared by concrete downloaders.
    """

    def __init__(
        self,
        config: ConfigT,
        response_adapter_resolver: ResponseAdapterResolver,
    ) -> None:

        self._config = config
        self._response_adapter_resolver = response_adapter_resolver      


    @property
    def capabilities(self) -> DownloaderCapabilities:
        return DownloaderCapabilities()
    @property
    def config(
        self,
    ) -> ConfigT:

        return self._config

    async def stream(
        self,
        context: RequestContext,
    ) -> DownloadResult:
        raise NotImplementedError(
            f"{type(self).__name__} "
            "does not support streaming.",
        )

    def build_request(
        self,
        context: RequestContext,
    ) -> DownloadRequest:

        return DownloadRequest.from_context(
            context,
        )


    def _set_result(
        self,
        context: RequestContext,
        response: RequestResponse,
    ) -> DownloadResult:

        context.transport_response = response
        profile = context.descriptor.profile
        status_code=response.status_code

        adapter = self._response_adapter_resolver.resolve(
            profile=profile,
            response=response,
        )

        return DownloadResult(
            response=adapter,
            success=(
                200
                <= status_code
                < 400
            ),
        )