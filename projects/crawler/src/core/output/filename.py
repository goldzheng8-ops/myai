from typing import Any

from core.output.model import DownloadResult
from core.template.manager.base import TemplateManager


class DownloadFilenameResolver:

    def __init__(
        self,
        template_manager: TemplateManager,
        template: str,
    ) -> None:
        self._template_manager = template_manager
        self._template = template

    def resolve(
        self,
        download: DownloadResult,
    ) -> str:

        context: dict[str, Any] = {
            "download": download,
        }

        filename = self._template_manager.render(
            self._template,
            context,
        )

        filename = filename.strip()

        if not filename:
            raise ValueError(
                "Resolved download filename is empty.",
            )

        return filename