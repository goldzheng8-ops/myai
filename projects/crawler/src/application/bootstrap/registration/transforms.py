from core.provider import ProviderBuilder
from core.extraction.transform import (
    TransformRegistry,
    TransformType,
    DateTimeTransform,
    JoinTransform,
    LowerTransform,
    NumberTransform,
    PrefixTransform,
    RegexTransform,
    ReplaceTransform,
    SplitTransform,
    StripTransform,
    SuffixTransform,
    ToFloatTransform,
    ToIntTransform,
    UpperTransform,
)


def register_transforms(
    builder: ProviderBuilder,
) -> None:

    builder.add_factory(
        TransformRegistry,
        lambda _: create_transform_registry(),
    )


def create_transform_registry() -> TransformRegistry:
    registry = TransformRegistry()

    registry.register(
        TransformType.DATETIME,
        DateTimeTransform,
    )

    registry.register(
        TransformType.JOIN,
        JoinTransform,
    )

    registry.register(
        TransformType.LOWER,
        LowerTransform,
    )

    registry.register(
        TransformType.NUMBER,
        NumberTransform,
    )

    registry.register(
        TransformType.PREFIX,
        PrefixTransform,
    )

    registry.register(
        TransformType.REGEX,
        RegexTransform,
    )

    registry.register(
        TransformType.REPLACE,
        ReplaceTransform,
    )

    registry.register(
        TransformType.SPLIT,
        SplitTransform,
    )

    registry.register(
        TransformType.STRIP,
        StripTransform,
    )

    registry.register(
        TransformType.SUFFIX,
        SuffixTransform,
    )

    registry.register(
        TransformType.TO_FLOAT,
        ToFloatTransform,
    )

    registry.register(
        TransformType.TO_INT,
        ToIntTransform,
    )

    registry.register(
        TransformType.UPPER,
        UpperTransform,
    )

    return registry