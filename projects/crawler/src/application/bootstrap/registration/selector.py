
from core.extraction.selector.extraction.attribute import AttributeExtractionStrategy
from core.extraction.selector.extraction.html import HtmlExtractionStrategy
from core.extraction.selector.extraction.mode import ExtractMode
from core.extraction.selector.extraction.registry import ExtractionRegistry
from core.extraction.selector.extraction.text import TextExtractionStrategy
from core.extraction.selector.selection.mode import SelectionMode
from core.extraction.selector.selection.multiple import MultipleSelectionStrategy
from core.extraction.selector.selection.registry import SelectionRegistry
from core.extraction.selector.selection.single import SingleSelectionStrategy
from core.provider import ProviderBuilder


def register_selector_registries(
    builder: ProviderBuilder,
) -> None:

    builder.add_factory(
        SelectionRegistry,
        lambda _: create_selection_registry(),
    )

    builder.add_factory(
        ExtractionRegistry,
        lambda _: create_extraction_registry(),
    )

def create_extraction_registry() -> ExtractionRegistry:
    registry = ExtractionRegistry()

    registry.register(
        ExtractMode.ATTRIBUTE,
        AttributeExtractionStrategy,
    )

    registry.register(
        ExtractMode.HTML,
        HtmlExtractionStrategy,
    )

    registry.register(
        ExtractMode.TEXT,
        TextExtractionStrategy,
    )

    return registry

def create_selection_registry() -> SelectionRegistry:
    registry = SelectionRegistry()

    registry.register(
        SelectionMode.SINGLE,
        SingleSelectionStrategy,
    )

    registry.register(
        SelectionMode.MULTIPLE,
        MultipleSelectionStrategy,
    )

    return registry