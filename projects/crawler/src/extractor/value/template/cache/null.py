

from typing import TypeVar

from extractor.value.template.cache.base import TemplateCache

T = TypeVar("T")

class NullTemplateCache(
    TemplateCache[T],
):

    def get(
        self,
        key: str,
    ) -> T | None:

        return None

    def put(
        self,
        key: str,
        value: T,
    ) -> None:

        pass

    def clear(
        self,
    ) -> None:

        pass