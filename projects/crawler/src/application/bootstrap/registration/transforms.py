from ...core.provider import ProviderBuilder
from ...transform import (
    TransformRegistry,
    TransformType,
    create_constant_transform,
    create_regex_transform,
    create_template_transform,
)


def register_transforms(
    builder: ProviderBuilder,
) -> None:

    builder.add_instance(
        TransformRegistry,
        create_transform_registry(),
    )


def create_transform_registry() -> TransformRegistry:

    registry = TransformRegistry()

    registry.register(
        TransformType.CONSTANT,
        create_constant_transform,
    )

    registry.register(
        TransformType.REGEX,
        create_regex_transform,
    )

    registry.register(
        TransformType.TEMPLATE,
        create_template_transform,
    )

    return registry