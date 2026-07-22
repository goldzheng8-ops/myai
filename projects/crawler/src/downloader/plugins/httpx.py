

from downloader.base import DownloaderPlugin
from downloader.config.enums import DownloaderType
from downloader.result import DownloadResult


class HttpxDownloader(DownloaderPlugin):
    """
    使用 httpx 库进行网页下载的插件。
    """
    type=DownloaderType.AIOHTTP
    def download(self, request: RequestContext) -> DownloadResult:
        """
        使用 httpx 下载网页，并返回统一的 ResponseAdapter。
        """
        import httpx

        with httpx.Client() as client:
            response = client.request(
                method=request.method,
                url=request.url,
                headers=request.headers,
                cookies=request.cookies,
                params=request.params,
                data=request.data,
                json=request.json,
                timeout=request.timeout,
            )

        return DownloadResult(
            status_code=response.status_code,
            headers=response.headers,
            content=response.content,
            text=response.text,
            url=str(response.url),
        )