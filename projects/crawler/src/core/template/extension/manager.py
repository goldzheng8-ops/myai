
from core.template.backend.base import TemplateBackend
from core.template.extension.registry import TemplateExtensionRegistry



class TemplateExtensionManager:

    def __init__(
        self,
        registry:
        TemplateExtensionRegistry,
    ):

        self._registry = registry

    def install(
        self,
        backend:
        TemplateBackend,
    ):

        for extension in self._registry.extensions():

            extension.install(
                backend,
            )