'''
实现
strip

lower

upper

capitalize

title

replace

truncate

slug

snake_case

camel_case

pascal_case

kebab_case

regex_replace
'''

from typing import Any

from core.template.extension.filter import FilterExtension


class UpperFilter(FilterExtension):
    name = "upper"

    def filter(self, value: Any) -> Any:
        if isinstance(value, str):
            return value.upper()
        return value