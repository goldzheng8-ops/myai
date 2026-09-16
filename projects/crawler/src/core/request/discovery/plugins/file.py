from pathlib import Path
from core.extraction.response import ResponseAdapter
from core.request.context import RequestContext
from core.request.discovery.config import FileDiscoveryConfig
from core.request.discovery.exception import DiscoveryError
from core.request.discovery.typing import DiscoveryType
from core.request.discovery.url.base import UrlDiscoveryPlugin

class FileDiscoveryPlugin(
    UrlDiscoveryPlugin[FileDiscoveryConfig],
):

    plugin_type = DiscoveryType.FILE
    config_type = FileDiscoveryConfig

    async def urls(
        self,
        *,
        response: ResponseAdapter,
        context: RequestContext,
        config: FileDiscoveryConfig,
    ) -> list[str]:

        path = Path(config.path)

        if not path.is_file():
            raise DiscoveryError(
                f"Discovery file not found: {path}",
            )

        try:
            text = path.read_text(
                encoding=config.encoding,
            )
        except OSError as exc:
            raise DiscoveryError(
                f"Failed to read discovery file: {path}",
            ) from exc

        urls: list[str] = []

        for line in text.splitlines():

            value = (
                line.strip()
                if config.strip
                else line
            )

            if config.skip_empty and not value:
                continue

            urls.append(value)

        return urls