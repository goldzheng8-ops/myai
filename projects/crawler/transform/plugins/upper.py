

from transform.base import TransformPlugin


class UpperTransform(TransformPlugin):
    name = "upper"

    def transform(self, value: str) -> str:
        return value.upper()