from __future__ import annotations
from typing import Protocol

from core.request.middleware.cookie.policy.model import CookieDomainResolution


class CookieDomainPolicy(Protocol):

    def resolve(
        self,
        *,
        request_host: str,
        domain_attribute: str | None,
    ) -> CookieDomainResolution:
        ...

class PublicSuffixMatcher(Protocol):
    def is_public_suffix(
        self,
        domain: str,
    ) -> bool:
        ...