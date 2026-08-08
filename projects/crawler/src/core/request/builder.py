from __future__ import annotations

from .typing import (
    RequestKind,
    HttpMethod,
)

from .descriptor import RequestDescriptor
from .meta import RequestMeta
from .profile import RequestProfile
from .typing import (
    RequestBody,
    RequestCookies,
    RequestHeaders,
    RequestParams,
)


class RequestBuilder:
    """
    Builder for RequestDescriptor.
    """

    def __init__(
        self,
        url: str,
        *,
        kind: RequestKind,
        profile: RequestProfile,
    ) -> None:

        self._url = url

        self._kind = kind

        self._profile = profile

        self._method = HttpMethod.GET

        self._headers: RequestHeaders = {}

        self._cookies: RequestCookies = {}

        self._params: RequestParams = {}

        self._body: RequestBody = None

        self._meta = RequestMeta()

    def method(
        self,
        method: HttpMethod,
    ) -> RequestBuilder:

        self._method = method

        return self

    def headers(
        self,
        headers: RequestHeaders,
    ) -> RequestBuilder:

        self._headers.update(headers)

        return self

    def cookies(
        self,
        cookies: RequestCookies,
    ) -> RequestBuilder:

        self._cookies.update(cookies)

        return self

    def params(
        self,
        params: RequestParams,
    ) -> RequestBuilder:

        self._params.update(params)

        return self

    def body(
        self,
        body: RequestBody,
    ) -> RequestBuilder:

        self._body = body

        return self

    def meta(
        self,
        meta: RequestMeta,
    ) -> RequestBuilder:

        self._meta = meta

        return self

    def build(
        self,
    ) -> RequestDescriptor:

        return RequestDescriptor(
            url=self._url,
            kind=self._kind,
            profile=self._profile,
            method=self._method,
            headers=dict(self._headers),
            cookies=dict(self._cookies),
            params=dict(self._params),
            body=self._body,
            meta=self._meta,
        )

    @classmethod
    def from_descriptor(
        cls,
        descriptor: RequestDescriptor,
    ) -> RequestBuilder:

        builder = cls(
            descriptor.url,
            kind=descriptor.kind,
            profile=descriptor.profile,
        )

        builder._method = descriptor.method

        builder._headers = dict(
            descriptor.headers,
        )

        builder._cookies = dict(
            descriptor.cookies,
        )

        builder._params = dict(
            descriptor.params,
        )

        builder._body = descriptor.body

        builder._meta = descriptor.meta

        return builder