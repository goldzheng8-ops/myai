
from selector.config.enums import SelectorType
from selector.base import SelectorPlugin


class CssSelectorPlugin(SelectorPlugin):

    type: SelectorType = SelectorType.CSS

    def select(self, response, config):
        return response.select(config)