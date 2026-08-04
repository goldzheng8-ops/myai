from abc import ABC
from typing import ClassVar, TypeVar

from core.cache.protocol import Cache
from core.plugin import Plugin


K = TypeVar("K")
V = TypeVar("V")


class CachePlugin(
    Plugin,
    Cache[K, V],
    ABC,
):

    type: ClassVar[str]