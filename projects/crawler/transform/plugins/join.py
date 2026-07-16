

from transform.base import TransformPlugin


class JoinTransform(TransformPlugin):
    name = "join"

    def apply(self, value, **kwargs):
        if isinstance(value, list):
            return " ".join(str(v) for v in value)
        return value