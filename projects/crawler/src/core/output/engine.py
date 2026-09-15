from collections.abc import Sequence

from core.output.model import DownloadResult, OutputItem
from core.output.resolver import OutputResolver


class OutputEngine:

    def __init__(
        self,
        output_resolver: OutputResolver,
    ) -> None:
        self._resolver = output_resolver

    async def write(
        self,
        item: OutputItem,
        outputs: Sequence[str],
    ) -> None:

        for name in outputs:
            sink = self._resolver.resolve(name)
            await sink.write(item)

    async def write_download(
        self,
        download: DownloadResult,
        outputs: Sequence[str],
    ) -> None:

        for name in outputs:
            sink = self._resolver.resolve(name)
            await sink.write_download(download)