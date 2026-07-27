from config.template.jinja import JinjaTemplateConfig
from extractor.value.template.backend.jinja import JinjaBackend
from extractor.value.template.cache.base import TemplateCache
from extractor.value.template.cache.memory import MemoryTemplateCache
from extractor.value.template.extension.manager import TemplateExtensionManager
from extractor.value.utils.object_context import ObjectContext
from extractor.value.utils.renderer import TemplateRenderer




from jinja2 import Template

class JinjaTemplateRenderer(
    TemplateRenderer,
):

    def __init__(
        self,
        manager: TemplateExtensionManager,
        config: JinjaTemplateConfig,
        cache: TemplateCache[Template] | None = None,
    ) -> None:

        environment = config.create_environment()

        backend = JinjaBackend(environment)

        manager.install(backend)

        self._environment = environment
        self._cache = cache or MemoryTemplateCache()

    def render(
        self,
        template: str,
        context: ObjectContext,
    ) -> str:

