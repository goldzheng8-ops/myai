from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass, field

from core.request.context import RequestContext
from core.request.typing import (
    HttpMethod,
    RequestBody,
    RequestCookies,
    RequestHeaders,
    RequestParams,
)


@dataclass(frozen=True, slots=True)
class DownloadRequest:
    """
    Transport-level request.

    This model represents the final request consumed by
    a downloader implementation.
    """

    url: str

    method: HttpMethod

    headers: RequestHeaders = field(
        default_factory=dict,
    )

    cookies: RequestCookies = field(
        default_factory=dict,
    )

    params: RequestParams = field(
        default_factory=dict,
    )

    body: RequestBody = None

    @classmethod
    def from_context(
        cls,
        context: RequestContext,
    ) -> DownloadRequest:

        descriptor = context.descriptor

        return cls(
            url=descriptor.url,
            method=descriptor.method,
            headers=dict(
                descriptor.headers,
            ),
            cookies=dict(
                descriptor.cookies,
            ),
            params=dict(
                descriptor.params,
            ),
            body=deepcopy(
                descriptor.body,
            ),
        )