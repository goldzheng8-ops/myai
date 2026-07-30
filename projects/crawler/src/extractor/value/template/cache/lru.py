
from cachetools import LRUCache
from extractor.value.template.adapter.base import RenderableTemplate
from extractor.value.template.cache.base import TemplateCache

class LruTemplateCache(
    TemplateCache,
):

    def __init__(
        self,
        maxsize: int = 512,
    ) -> None:

        self._cache: LRUCache[
            str,
            RenderableTemplate,
        ] = LRUCache(maxsize=maxsize)

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

    def clear(self) -> None:

        self._cache.clear()