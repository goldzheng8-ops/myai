from pathlib import Path
from urllib.parse import urlparse
from uuid import uuid4

from core.output.config import BinaryFileOutputConfig
from core.output.model import DownloadResult, OutputItem
from core.output.sink.base import OutputSink


class BinaryFileOutputSink(
    OutputSink[BinaryFileOutputConfig],
):

    def __init__(
        self,
        config: BinaryFileOutputConfig,
    ) -> None:
        super().__init__(config)
        self._directory: Path | None = None

    async def start(self) -> None:
        if self._directory is not None:
            return

        directory = Path(
            self.config.directory,
        )

        directory.mkdir(
            parents=True,
            exist_ok=True,
        )

        self._directory = directory

    async def write(
        self,
        item: OutputItem,
    ) -> None:
        raise TypeError(
            "BinaryFileOutputSink does not support "
            "OutputItem.",
        )

    async def write_download(
        self,
        download: DownloadResult,
    ) -> None:
        if self._directory is None:
            raise RuntimeError(
                "BinaryFileOutputSink is not open.",
            )

        filename = self._resolve_filename(
            download,
        )

        path = self._directory / filename

        if (
            path.exists()
            and not self.config.overwrite
        ):
            path = self._unique_path(path)

        path.write_bytes(download.body)

    async def close(self) -> None:
        self._directory = None

    def _resolve_filename(
        self,
        download: DownloadResult,
    ) -> str:
        if download.filename:
            return download.filename

        parsed = urlparse(download.url)
        name = Path(parsed.path).name

        if name:
            return name

        return f"download-{uuid4().hex}"

    @staticmethod
    def _unique_path(
        path: Path,
    ) -> Path:
        stem = path.stem
        suffix = path.suffix

        index = 1

        while True:
            candidate = path.with_name(
                f"{stem}-{index}{suffix}",
            )

            if not candidate.exists():
                return candidate

            index += 1