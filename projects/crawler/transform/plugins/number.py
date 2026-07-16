

from transform.base import TransformPlugin


class NumberTransform(TransformPlugin):
    name = "number"

    def apply(self, value, **kwargs):
        try:
            return float(value)
        except ValueError:
            return value