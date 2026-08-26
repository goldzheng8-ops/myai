
from core.template.backend.base import TemplateBackend
from core.template.extension.registry import TemplateExtensionRegistry



class TemplateExtensionManager:

    def __init__(
        self,
        registry:
        TemplateExtensionRegistry,
    ) -> None:

        self._registry = registry

    def install(
        self,
        backend:TemplateBackend,
    ) -> None:

        for key in self._registry.keys():
            extension=self._registry.create(key)

            extension.install(
                backend,
            )