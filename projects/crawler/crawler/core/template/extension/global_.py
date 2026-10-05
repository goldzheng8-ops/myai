from abc import abstractmethod
from typing import Any, ClassVar


from core.template.backend.base import TemplateBackend
from core.template.extension.base import TemplateExtension
from core.template.typing import ExtensionKind

class GlobalExtension(
    TemplateExtension,
):
    plugin_type = ExtensionKind.GLOBAL
    name: ClassVar[str]

    @abstractmethod
    def global_(
        self,
        value: Any,
    ) -> Any:
        ...

    def install(
        self,
        backend: TemplateBackend,
    ) -> None:

        # try:
        backend.globals.register(
            self.name,
            self.global_,
        )
        # except ValueError:
        #     # global already registered by the backend; skip to avoid crash
        #     return