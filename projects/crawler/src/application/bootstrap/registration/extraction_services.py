
from core.extraction.extractor.engine import ExtractEngine
from core.provider import ProviderBuilder
from core.request.discovery.engine import DiscoveryEngine


def register_extraction_services(
    builder: ProviderBuilder,
) -> None:

    builder.add_type(
        ExtractEngine,
    )

    builder.add_type(
        DiscoveryEngine,
    )