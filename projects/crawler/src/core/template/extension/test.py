from abc import abstractmethod
from typing import Any, ClassVar


from core.template.backend.base import TemplateBackend
from core.template.extension.base import TemplateExtension
from core.template.typing import ExtensionKind

class TestExtension(
    TemplateExtension,
):
    plugin_type = ExtensionKind.TEST
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

        # try:
        backend.tests.register(
            self.name,
            self.test,
        )
        # except ValueError:
        #     # test already registered by the backend; skip to avoid crash
        #     return