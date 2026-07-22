

from downloader.config.enums import DownloaderType
from downloader.result import DownloadResult


class AiohttpDownloaderPlugin(DownloaderPlugin):
    """
    使用 aiohttp 进行异步下载的插件。
    """
    type=DownloaderType.AIOHTTP
    async def download(
        self,
        request: RequestContext,
    ) -> DownloadResult:
        """
        使用 aiohttp 下载网页，并返回统一的 ResponseAdapter。
        """
        import aiohttp

        async with aiohttp.ClientSession() as session:
            async with session.request(
                method=request.method,
                url=request.url,
                headers=request.headers,
                cookies=request.cookies,
            ) as response:
                content = await response.read()
                return DownloadResult(
                    status_code=response.status,
                    headers=dict(response.headers),
                    content=content,
                    url=str(response.url),
                )