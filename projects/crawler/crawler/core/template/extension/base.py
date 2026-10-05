from abc import ABC, abstractmethod
from typing import ClassVar

from core.plugin import Plugin
from core.template.backend.base import TemplateBackend
from core.template.typing import ExtensionKind




class TemplateExtension(
    Plugin,
    ABC,
):
    plugin_type: ClassVar[ExtensionKind]
    name: ClassVar[str]

    @abstractmethod
    def install(
        self,
        backend: TemplateBackend,
    ) -> None:
        ...