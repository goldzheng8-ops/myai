from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Proxy:
    url: str
    country: str | None = None

