
from scrapy.http import Response


from adapters.base import ResponseAdapter

from scrapy.selector import Selector

class ScrapyResponseAdapter(ResponseAdapter):

    def __init__(self, node: Response | Selector):
        self._node = node

class ScrapyResponseAdapter(ResponseAdapter):

    def html(self) -> str:
        return self.response.text

    def text(self) -> str:
        return self.response.xpath("string(.)").get("") or ""

    def json(self) -> Any:
        return json.loads(self.response.text)


