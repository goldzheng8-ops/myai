

from transform.base import TransformPlugin


class SplitTransform(TransformPlugin):
    name = "split"

    def apply(self, value: str, delimiter: str = ",") -> list:
        if not isinstance(value, str):
            raise ValueError("Input value must be a string.")
        return value.split(delimiter)