

from transform.base import TransformPlugin


class RegexTransform(TransformPlugin):
    name = "regex"

    def apply(self, value, pattern, replacement="", **kwargs):
        import re

        if isinstance(value, str):
            return re.sub(pattern, replacement, value)
        return value