from pathlib import Path

from core.output.config import BinaryFileOutputConfig
from core.output.filename import DownloadFilenameResolver
from core.output.model import DownloadArtifact, OutputItem
from core.output.sink.base import OutputSink
from core.output.storage.base import Storage


class BinaryFileOutputSink(
    OutputSink[BinaryFileOutputConfig],
):

    def __init__(
        self,
        config: BinaryFileOutputConfig,
        filename_resolver: DownloadFilenameResolver,
        storage: Storage,
    ) -> None:

        super().__init__(config)

        self._filename_resolver = (
            filename_resolver
        )

        self._storage = storage

    async def start(self) -> None:
        await self._storage.start()

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
        download: DownloadArtifact,
    ) -> None:

        filename = self._filename_resolver.resolve(
            download=download,
        )

        filename = await self._resolve_collision(
            filename,
        )

        if download.body.body_stream is not None:

            await self._storage.write_stream(
                key=filename,
                body=download.body.body_stream,
                overwrite=self.config.overwrite,
                content_type=download.content_type,
                metadata=self._build_metadata(
                    download,
                ),
            )

            return

        if download.body.body_bytes is not None:

            await self._storage.write_bytes(
                key=filename,
                body=download.body.body_bytes,
                overwrite=self.config.overwrite,
                content_type=download.content_type,
                metadata=self._build_metadata(
                    download,
                ),
            )

            return

        raise RuntimeError(
            "DownloadArtifact contains neither "
            "body_bytes nor body_stream.",
        )

    @staticmethod
    def _build_metadata(
        download: DownloadArtifact,
    ) -> dict[str, str]:

        return {
            str(key): str(value)
            for key, value in download.metadata.items()
        }

    async def close(self) -> None:
        await self._storage.close()

    async def _resolve_collision(
        self,
        filename: str,
    ) -> str:

        if self.config.overwrite:
            return filename

        if not await self._storage.exists(
            filename,
        ):
            return filename

        path = Path(filename)

        stem = path.stem
        suffix = path.suffix

        index = 1

        while True:

            candidate = (
                f"{stem}-{index}{suffix}"
            )

            if not await self._storage.exists(
                candidate,
            ):
                return candidate

            index += 1