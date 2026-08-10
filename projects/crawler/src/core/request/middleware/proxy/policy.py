from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ProxyPolicy:

    enabled: bool = True

    override: bool = False