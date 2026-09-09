from core.extraction.transform.engine import TransformEngine
from core.extraction.transform.executor import TransformExecutor
from core.extraction.transform.plugins.datetime import DateTimeTransform
from core.extraction.transform.plugins.join import JoinTransform
from core.extraction.transform.plugins.lower import LowerTransform
from core.extraction.transform.plugins.number import NumberTransform
from core.extraction.transform.plugins.prefix import PrefixTransform
from core.extraction.transform.plugins.regex import RegexTransform
from core.extraction.transform.plugins.replace import ReplaceTransform
from core.extraction.transform.plugins.split import SplitTransform
from core.extraction.transform.plugins.strip import StripTransform
from core.extraction.transform.plugins.suffix import SuffixTransform
from core.extraction.transform.plugins.to_float import ToFloatTransform
from core.extraction.transform.plugins.to_int import ToIntTransform
from core.extraction.transform.plugins.upper import UpperTransform
from core.extraction.transform.registry import TransformRegistry
from core.extraction.transform.typing import TransformType
from core.provider import ProviderBuilder


def register_transforms(
    builder: ProviderBuilder,
) -> None:

    builder.add_factory(
        TransformRegistry,
        lambda _: create_transform_registry(),
    )

    builder.add_factory(
        TransformExecutor,
        lambda resolver: TransformEngine(
            registry=resolver.resolve(
                TransformRegistry,
            ),
        ),     
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