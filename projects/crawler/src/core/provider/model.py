from dataclasses import dataclass
from typing import Any

from core.provider.base import BaseProvider
from core.provider.typing import ProviderFactory

@dataclass(frozen=True, slots=True)
class ProviderRegistration:
    factory: ProviderFactory[Any]
    strategy_cls: type[BaseProvider] | None = None