from core.template.extension.manager import TemplateExtensionManager
from core.template.backend.config import JinjaTemplateConfig
from core.template.typing import TemplateBackendType
from core.template.adapter.jinja import JinjaRenderableTemplate
from core.template.backend.registry import  FilterRegistry, GlobalRegistry, TestRegistry


from core.template.backend.base import TemplateBackend
from core.template.adapter.base import RenderableTemplate

class JinjaBackend(
    TemplateBackend,
):
    plugin_type = TemplateBackendType.JINJA

    def __init__(
        self,
        config: JinjaTemplateConfig,
        extensions: TemplateExtensionManager,
    ) -> None:
        
        self._environment = config.create_environment()

        self._filters = FilterRegistry(
            self._environment.filters,
        )

        self._tests = TestRegistry(
            self._environment.tests,
        )

        self._globals = GlobalRegistry(
            self._environment.globals,
        )

        extensions.install(
            self,
        )

    @property
    def filters(
        self,
    ) -> FilterRegistry:

        return self._filters
    
    @property
    def tests(
        self,
    ) -> TestRegistry:

        return self._tests
    
    @property
    def globals(
        self,
    ) -> GlobalRegistry:

        return self._globals

    def compile(
        self,
        source: str,
    ) -> RenderableTemplate:

        template = self._environment.from_string(
            source,
        )

        return JinjaRenderableTemplate(
            source,
            template,
        )