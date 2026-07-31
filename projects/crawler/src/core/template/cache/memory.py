
from collections.abc import MutableMapping

from core.template.adapter.base import RenderableTemplate
from core.template.cache.base import TemplateCache


class MemoryTemplateCache(
    TemplateCache,
):

    def __init__(
        self,
        cache: MutableMapping[str, RenderableTemplate] | None = None,
    ) -> None:

        self._cache: dict[
            str,
            RenderableTemplate,
        ] = {}

    def get(
        self,
        key: str,
    ) -> RenderableTemplate | None:

        return self._cache.get(key)

    def put(
        self,
        key: str,
        template: RenderableTemplate,
    ) -> None:

        self._cache[key] = template

    def clear(
        self,
    ) -> None:

        self._cache.clear()