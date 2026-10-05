from dataclasses import dataclass

@dataclass(frozen=True, slots=True)
class CookieDomainResolution:
    scope_domain: str
    host_only: bool