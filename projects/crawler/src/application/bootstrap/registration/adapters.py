from core.extraction.response.factory import ResponseAdapterFactory
from core.provider import ProviderBuilder


def register_adapters(
    builder: ProviderBuilder,
) -> None:

    builder.add_type(
        ResponseAdapterFactory,
    )