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

        # try:
        backend.filters.register(
            self.name,
            self.filter,
        )
        # except ValueError:
        #     # filter already registered by the backend (e.g. built-in Jinja filter);
        #     # skip registering to avoid crashing on duplicate names.
        #     return