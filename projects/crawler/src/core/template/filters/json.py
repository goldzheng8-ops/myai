import json
from typing import Any

from core.template.extension.filter import FilterExtension


class JsonFilter(FilterExtension):
    name = "json"

    def filter(self, value: Any) -> Any:
        return json.dumps(value, ensure_ascii=False)


class PrettyJsonFilter(FilterExtension):
    name = "pretty_json"

    def filter(self, value: Any) -> Any:
        return json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True)


class FromJsonFilter(FilterExtension):
    name = "from_json"

    def filter(self, value: Any) -> Any:
        if value is None:
            return None
        if isinstance(value, (dict, list, int, float, bool)):
            return value
        return json.loads(str(value))
