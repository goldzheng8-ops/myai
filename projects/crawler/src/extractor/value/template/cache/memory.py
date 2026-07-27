
from collections.abc import MutableMapping
from typing import TypeVar

from extractor.value.template.cache.base import TemplateCache
T = TypeVar("T")

class MemoryTemplateCache(
    TemplateCache[T],
):

    def __init__(
        self,
        cache: MutableMapping[str, T] | None = None,
    ) -> None:

        self._cache = cache or {}

    def get(
        self,
        key: str,
    ) -> T | None:

        return self._cache.get(key)

    def put(
        self,
        key: str,
        value: T,
    ) -> None:

        self._cache[key] = value

    def clear(
        self,
    ) -> None:

        self._cache.clear()