from transform.registry import registry as transform_registry

from config.config import TransformConfig

class TransformEngine:

    def __init__(self):

        self.registry = transform_registry
    def execute(
        self,
        value:str,
        configs: list[TransformConfig],
    ) -> str:

        result = value

        for config in configs:

            transform = self.registry.get(config.type)

            result = transform.apply(
                result,
                *config.args,
            )

        return result