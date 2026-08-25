from core.runtime import RuntimeContext
from core.template.adapter.base import RenderableTemplate
from core.template.backend.base import TemplateBackend
from core.template.cache.base import TemplateCache
from core.template.manager.base import TemplateManager


class DefaultTemplateManager(
    TemplateManager,
):

    def __init__(
        self,
        backend: TemplateBackend,
        cache: TemplateCache,
    ) -> None:

        self._backend = backend
        self._cache = cache

    def load(
        self,
        source: str,
    ) -> RenderableTemplate:

        template = self._cache.get(source)

        if template is None:

            template = self._backend.compile(
                source,
            )

            self._cache.put(
                source,
                template,
            )

        return template

    def render(
        self,
        template: str,
        context: RuntimeContext,
    ) -> str:

        return self.load(
            template,
        ).render(
            context,
        )