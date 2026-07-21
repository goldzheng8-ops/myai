


from selector.base import SelectorPlugin


class SelectorRegistry:
    def __init__(self):
        self._plugins = dict[str, SelectorPlugin]()

    def register(self, plugin:SelectorPlugin):
        self._plugins[plugin.type] = plugin

    def get(self, name:str) -> SelectorPlugin:
        return self._plugins[name]
    




