from downloader.base import DownloaderPlugin
from extractor.extractor import ExtractorEngine
from runner.base import BaseRunner


class SingleRunner(BaseRunner):

    def __init__(
        self,
        downloader: DownloaderPlugin,
        extractor: ExtractorEngine,
    ):
        self.downloader = downloader
        self.extractor = extractor

    async def start(self):
        await self.downloader.start()

    async def close(self):
        await self.downloader.close()

    async def run(self, context: RequestContext):

        download_result = await self.downloader.download(context)

        return self.extractor.extract(
            response=download_result.response,
            configs=context.config.extractors,
        )