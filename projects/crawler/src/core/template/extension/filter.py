from abc import abstractmethod
from typing import Any, ClassVar


from core.template.backend.base import TemplateBackend
from core.template.extension.base import TemplateExtension
from core.template.typing import ExtensionKind

class FilterExtension(
    TemplateExtension,
):
    plugin_type = ExtensionKind.FILTER
    name: ClassVar[str]

    @abstractmethod
    def filter(
        self,
        value: Any,
    ) -> Any:
        ...

    def install(
        self,
        backend: TemplateBackend,
    ) -> None:

        backend.filters.register(
            self.name,
            self.filter,
        )