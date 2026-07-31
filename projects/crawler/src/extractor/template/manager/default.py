from extractor.template.adapter.base import RenderableTemplate
from extractor.template.backend.base import TemplateBackend
from extractor.template.cache.base import TemplateCache
from extractor.template.manager.base import TemplateManager


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