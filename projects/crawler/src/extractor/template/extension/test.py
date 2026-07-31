from abc import abstractmethod
from typing import Any, ClassVar


from extractor.template.backend.base import TemplateBackend
from extractor.template.extension.base import TemplateExtension

class TestExtension(
    TemplateExtension,
):

    name: ClassVar[str]

    @abstractmethod
    def test(
        self,
        value: Any,
    ) -> Any:
        ...

    def install(
        self,
        backend: TemplateBackend,
    ) -> None:

        backend.tests.register(
            self.name,
            self.test,
        )