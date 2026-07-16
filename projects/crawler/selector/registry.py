


from selector.base import SelectorPlugin
from selector.plugins.css import CssSelector
from selector.plugins.jsonpath import JsonPathSelector
from selector.plugins.regex import RegexSelector
from selector.plugins.xpath import XPathSelector


class SelectorRegistry:
    def __init__(self):
        self._plugins = dict[str, SelectorPlugin]()

    def register(self, plugin:SelectorPlugin):
        self._plugins[plugin.name] = plugin

    def get(self, name:str) -> SelectorPlugin:
        return self._plugins[name]
    




registry = SelectorRegistry()
registry.register(CssSelector())

registry.register(XPathSelector())

registry.register(RegexSelector())

registry.register(JsonPathSelector())