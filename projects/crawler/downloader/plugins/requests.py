

import requests

from downloader.base import DownloaderPlugin
from downloader.result import DownloadResult
from request.context import RequestContext


class RequestsDownloader(
    DownloaderPlugin,
):

    def download(
        self,
        request: RequestContext,
    ) -> DownloadResult:

        response = requests.request(
            method=request.method,
            url=request.url,
            headers=request.headers,
            cookies=request.cookies,
            data=request.data,
            params=request.params,
        )

        return DownloadResult(
            response=response,
        )