from __future__ import annotations

from typing import Protocol
from urllib.parse import urlsplit

from core.request.context import RequestContext


class ThrottleKeyResolver(Protocol):
    """
    Resolve the throttling key for a request.

    The key identifies the resource scope that should
    share the same throttling state.
    """

    def resolve(
        self,
        context: RequestContext,
    ) -> str:
        ...

class HostThrottleKeyResolver(ThrottleKeyResolver):
    """
    Resolve the throttling key from the request URL hostname.
    """

    def resolve(
        self,
        context: RequestContext,
    ) -> str:

        url = context.descriptor.url

        parsed = urlsplit(url)

        hostname = parsed.hostname

        if not hostname:
            raise ValueError(
                f"Unable to resolve hostname "
                f"from request URL: {url!r}"
            )

        return hostname.lower()

