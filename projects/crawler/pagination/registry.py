

from pagination.base import PaginationPlugin


class PaginationRegistry:

    def __init__(self):
        self._registry = dict[str, PaginationPlugin]()

    def register(self, plugin_type:str, plugin:PaginationPlugin):
        self._registry[plugin_type] = plugin

    def get(self, plugin_type:str) -> PaginationPlugin:
        return self._registry[plugin_type]