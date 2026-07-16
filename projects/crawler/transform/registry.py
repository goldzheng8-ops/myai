from transform.base import TransformPlugin
from transform.plugins.datetime import DateTimeTransform
from transform.plugins.strip import StripTransform
from transform.plugins.replace import ReplaceTransform
from transform.plugins.number import NumberTransform



class TransformRegistry:

    def __init__(self):
        self._plugins = dict[str, TransformPlugin]()

    def register(self, plugin : TransformPlugin):

        self._plugins[plugin.name] = plugin  

    def get(self, name:str) -> TransformPlugin:

        return self._plugins[name]  
    
registry = TransformRegistry()
registry.register(StripTransform())

registry.register(ReplaceTransform())

registry.register(NumberTransform())

registry.register(DateTimeTransform())