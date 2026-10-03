
from core.lifecycle.manager import LifecycleManager
from core.provider.builder import ProviderBuilder


def register_lifecycle(
    builder: ProviderBuilder,
) -> None:

    builder.add_type(
        LifecycleManager,
    )