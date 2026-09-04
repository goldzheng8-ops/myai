from core.extraction.response.resolver import ResponseAdapterResolver
from core.provider import ProviderBuilder


def register_adapters(
    builder: ProviderBuilder,
) -> None:

    builder.add_type(
        ResponseAdapterResolver,
    )