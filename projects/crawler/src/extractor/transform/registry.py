from typing import Any

from transform.base import TransformPlugin
from transform.config.enums import TransformType


class TransformRegistry:

    def __init__(self):
        self._plugins = dict[TransformType, TransformPlugin[Any,Any]]()

    def register(self, plugin: TransformPlugin[Any,Any]):
        self._plugins[plugin.type] = plugin

    def get(self, type:TransformType) -> TransformPlugin[Any,Any]:
        return self._plugins[type]