from abc import abstractmethod
from typing import Any, ClassVar


from extractor.value.template.backend.base import TemplateBackend
from extractor.value.template.extension.base import TemplateExtension

class GlobalExtension(
    TemplateExtension,
):

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

        backend.globals.register(
            self.name,
            self.global_,
        )