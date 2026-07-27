from abc import abstractmethod
from typing import Any, ClassVar


from extractor.value.template.backend.base import TemplateBackend
from extractor.value.template.extension.base import TemplateExtension

class FilterExtension(
    TemplateExtension,
):

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