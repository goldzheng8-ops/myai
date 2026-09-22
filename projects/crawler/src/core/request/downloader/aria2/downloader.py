import asyncio
from pathlib import Path
import shutil
import tempfile

from core.extraction.response.resolver import ResponseAdapterResolver
from core.request.download.exception import DownloadError
from core.request.downloader.aria2.launcher import Aria2ProcessLauncher
from core.request.downloader.aria2.model import Aria2DownloadResult, Aria2Status
from core.request.downloader.aria2.monitor import Aria2DownloadMonitor
from core.request.downloader.aria2.options import Aria2OptionsBuilder
from core.extraction.response.base import ResponseAdapter
from core.request.response.model import Aria2Response
from core.request.typing import DownloaderType
from core.request.downloader.base import BaseDownloader
from core.request.downloader.model import DownloaderCapabilities
from core.request.downloader.result import DownloadResult
from core.request.context import RequestContext
from ..config import Aria2DownloaderConfig
from .client import Aria2Client

class Aria2Downloader(
    BaseDownloader[Aria2DownloaderConfig],
):

    type = DownloaderType.ARIA2

    def __init__(
        self,
        response_adapter_resolver: ResponseAdapterResolver,
        client: Aria2Client,
        monitor: Aria2DownloadMonitor,
        options_builder: Aria2OptionsBuilder,
        launcher: Aria2ProcessLauncher,
        config: Aria2DownloaderConfig | None = None,
    ) -> None:

        super().__init__(
            config
            if config is not None
            else Aria2DownloaderConfig(),
        )

        self._response_adapter_resolver = (
            response_adapter_resolver
        )

        self._client = client
        self._monitor = monitor
        self._options_builder = options_builder
        self._launcher = launcher
        self._temp_directory: Path | None = None

    @property
    def capabilities(
        self,
    ) -> DownloaderCapabilities:

        return DownloaderCapabilities(
            supports_resumable=True,
            supports_streaming=False,
            supports_range=True,
        )

    async def start(self) -> None:

        await self._launcher.start()
        await self._client.start()

        if self._temp_directory is not None:
            return

        self._temp_directory = Path(
            tempfile.mkdtemp(
                prefix="ai-space-aria2-",
            ),
        )

    async def close(self) -> None:
        await self._client.close()
        await self._launcher.close()
        directory = self._temp_directory

        self._temp_directory = None

        if directory is not None:
            await asyncio.to_thread(
                shutil.rmtree,
                directory,
                ignore_errors=True,
            )

    async def download(
        self,
        context: RequestContext,
    ) -> DownloadResult:

        directory = self._require_temp_directory()

        task_directory = Path(
            tempfile.mkdtemp(
                prefix="download-",
                dir=directory,
            ),
        )

        try:

            return await self._download_from_aria2(
                context=context,
                task_directory=task_directory,
            )

        finally:

            await asyncio.to_thread(
                shutil.rmtree,
                task_directory,
                ignore_errors=True,
            )


    def _require_temp_directory(self) -> Path:

        directory = self._temp_directory

        if directory is None:
            raise RuntimeError(
                "Aria2Downloader is not started.",
            )

        return directory

    async def _build_response(
        self,
        *,
        context: RequestContext,
        result: Aria2DownloadResult,
    ) -> ResponseAdapter:

        if not result.files:
            raise DownloadError(
                "Aria2 completed without producing a file.",
                url=context.descriptor.url,
            )

        if len(result.files) != 1:
            raise DownloadError(
                "Aria2 download produced "
                f"{len(result.files)} files; "
                "single-file download expected.",
                url=context.descriptor.url,
            )

        file = result.files[0]

        path = Path(file.path)

        if not path.is_file():
            raise DownloadError(
                "Aria2 output file does not exist: "
                f"{path}",
                url=context.descriptor.url,
            )

        body = await asyncio.to_thread(
            path.read_bytes,
        )

        response = Aria2Response(
            url=context.descriptor.url,
            status_code=200,
            headers={
                "content-length": str(len(body)),
            },
            body=body,
            encoding=None,
            reason="OK",
        )

        return self._response_adapter_resolver.resolve(
            profile=context.descriptor.profile,
            response=response,
        )


    async def _download_from_aria2(
        self,
        *,
        context: RequestContext,
        task_directory: Path,
    ) -> DownloadResult:

        options = self._options_builder.build(
            context,
            directory=str(task_directory),
        )

        gid: str | None = None

        try:

            gid = await self._client.add_uri(
                uri=context.descriptor.url,
                options=options.to_rpc_options(),
            )

            result = await self._monitor.wait(
                gid,
            )

        except Exception as exc:

            return DownloadResult(
                success=False,
                error=exc,
                meta={
                    "download_strategy": "aria2",
                    "gid": gid,
                },
            )

        if result.status.status != Aria2Status.COMPLETE:

            return DownloadResult(
                success=False,
                error=DownloadError(
                    result.error_message
                    or "Aria2 download failed.",
                    url=context.descriptor.url,
                ),
                meta={
                    "gid": gid,
                    "aria2_error_code": result.error_code,
                },
            )

        try:

            response = await self._build_response(
                context=context,
                result=result,
            )

        except Exception as exc:

            return DownloadResult(
                success=False,
                error=DownloadError(
                    "Failed to build Aria2 response.",
                    url=context.descriptor.url,
                    cause=exc,
                ),
                meta={
                    "gid": gid,
                },
            )

        return DownloadResult(
            response=response,
            success=True,
            meta={
                "gid": gid,
                "download_strategy": "aria2",
            },
        )