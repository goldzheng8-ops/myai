from __future__ import annotations

from copy import deepcopy
from dataclasses import replace
from typing import Any, Mapping

from models.config.request import RequestConfig
from core.request.meta import RequestMeta

from .descriptor import RequestDescriptor
from .patch import RequestPatch
from .typing import (
    RequestKind,
    HttpMethod,
)
from .profile import RequestProfile


class RequestBuilder:
    """
    Factory/Builder for immutable RequestDescriptor.

    All shortcut methods delegate to `create()`.
    """

    @classmethod
    def create(
        cls,
        *,
        url: str,
        kind: RequestKind,
        profile: RequestProfile,
        method: HttpMethod = HttpMethod.GET,
        headers: Mapping[str, str] | None = None,
        cookies: Mapping[str, str] | None = None,
        params: Mapping[str, Any] | None = None,
        body: Any = None,
        meta: RequestMeta | None = None,
    ) -> RequestDescriptor:

        return RequestDescriptor(
            url=url,
            kind=kind,
            profile=profile,
            method=method,
            headers=dict(headers or {}),
            cookies=dict(cookies or {}),
            params=dict(params or {}),
            body=deepcopy(body),
            meta=deepcopy(meta)
            if meta is not None
            else RequestMeta(),
        )

    # ---------------------------------------------------------
    # shortcut builders
    # ---------------------------------------------------------

    @classmethod
    def detail(
        cls,
        *,
        url: str,
        profile: RequestProfile,
        method: HttpMethod = HttpMethod.GET,
        headers: Mapping[str, str] | None = None,
        cookies: Mapping[str, str] | None = None,
        params: Mapping[str, Any] | None = None,
        body: Any = None,
        meta: RequestMeta | None = None,
    ) -> RequestDescriptor:

        return cls.create(
            url=url,
            kind=RequestKind.DETAIL,
            profile=profile,
            method=method,
            headers=headers,
            cookies=cookies,
            params=params,
            body=body,
            meta=meta,
        )

    @classmethod
    def list(
        cls,
        *,
        url: str,
        profile: RequestProfile,
        method: HttpMethod = HttpMethod.GET,
        headers: Mapping[str, str] | None = None,
        cookies: Mapping[str, str] | None = None,
        params: Mapping[str, Any] | None = None,
        body: Any = None,
        meta: RequestMeta | None = None,
    ) -> RequestDescriptor:

        return cls.create(
            url=url,
            kind=RequestKind.LIST,
            profile=profile,
            method=method,
            headers=headers,
            cookies=cookies,
            params=params,
            body=body,
            meta=meta,
        )

    @classmethod
    def api(
        cls,
        *,
        url: str,
        profile: RequestProfile,
        method: HttpMethod = HttpMethod.GET,
        headers: Mapping[str, str] | None = None,
        cookies: Mapping[str, str] | None = None,
        params: Mapping[str, Any] | None = None,
        body: Any = None,
        meta: RequestMeta | None = None,
    ) -> RequestDescriptor:

        return cls.create(
            url=url,
            kind=RequestKind.API,
            profile=profile,
            method=method,
            headers=headers,
            cookies=cookies,
            params=params,
            body=body,
            meta=meta,
        )

    @classmethod
    def login(
        cls,
        *,
        url: str,
        profile: RequestProfile,
        method: HttpMethod = HttpMethod.GET,
        headers: Mapping[str, str] | None = None,
        cookies: Mapping[str, str] | None = None,
        params: Mapping[str, Any] | None = None,
        body: Any = None,
        meta: RequestMeta | None = None,
    ) -> RequestDescriptor:

        return cls.create(
            url=url,
            kind=RequestKind.LOGIN,
            profile=profile,
            method=method,
            headers=headers,
            cookies=cookies,
            params=params,
            body=body,
            meta=meta,
        )

    @classmethod
    def download(
        cls,
        *,
        url: str,
        profile: RequestProfile,
        method: HttpMethod = HttpMethod.GET,
        headers: Mapping[str, str] | None = None,
        cookies: Mapping[str, str] | None = None,
        params: Mapping[str, Any] | None = None,
        body: Any = None,
        meta: RequestMeta | None = None,
    ) -> RequestDescriptor:

        return cls.create(
            url=url,
            kind=RequestKind.DOWNLOAD,
            profile=profile,
            method=method,
            headers=headers,
            cookies=cookies,
            params=params,
            body=body,
            meta=meta,
        )




    # ---------------------------------------------------------
    # derived builders
    # ---------------------------------------------------------

    @classmethod
    def from_request(
        cls,
        request: RequestConfig,
        *,
        kind: RequestKind,
        profile: RequestProfile,
        meta: RequestMeta | None = None,
    ) -> RequestDescriptor:

        return cls.create(
            url=request.url,
            kind=kind,
            profile=profile,
            method=request.method,
            headers=request.headers,
            cookies=request.cookies,
            params=request.params,
            body=request.body,
            meta=meta,
        )

    @classmethod
    def from_patch(
        cls,
        *,
        descriptor: RequestDescriptor,
        patch: RequestPatch,
    ) -> RequestDescriptor:

        return cls.create(
            url=patch.url or descriptor.url,
            kind=descriptor.kind,
            profile=descriptor.profile,
            method=descriptor.method,
            headers=descriptor.headers,
            cookies=descriptor.cookies,
            params=(
                dict(patch.params)
                if patch.params is not None
                else descriptor.params
            ),
            body=(
                deepcopy(patch.body)
                if patch.body is not None
                else descriptor.body
            ),
            meta=deepcopy(descriptor.meta),
        )

    # ---------------------------------------------------------
    # utilities
    # ---------------------------------------------------------

    @classmethod
    def clone(
        cls,
        descriptor: RequestDescriptor,
    ) -> RequestDescriptor:

        return deepcopy(descriptor)

    @classmethod
    def replace(
        cls,
        descriptor: RequestDescriptor,
        **changes: Any,
    ) -> RequestDescriptor:

        return replace(
            descriptor,
            **changes,
        )

    @classmethod
    def replace_meta(
        cls,
        descriptor: RequestDescriptor,
        **changes: Any,
    ) -> RequestDescriptor:

        return replace(
            descriptor,
            meta=replace(
                descriptor.meta,
                **changes,
            ),
        )

    @classmethod
    def with_tag(
        cls,
        descriptor: RequestDescriptor,
        tag: str,
    ) -> RequestDescriptor:

        tags = set(descriptor.meta.tags)

        tags.add(tag)

        return cls.replace_meta(
            descriptor,
            tags=tags,
        )

    @classmethod
    def with_extra(
        cls,
        descriptor: RequestDescriptor,
        key: str,
        value: Any,
    ) -> RequestDescriptor:

        extras = dict(
            descriptor.meta.extras,
        )

        extras[key] = value

        return cls.replace_meta(
            descriptor,
            extras=extras,
        )

    @classmethod
    def without_tag(
        cls,
        descriptor: RequestDescriptor,
        tag: str,
    ) -> RequestDescriptor:

        tags = set(
            descriptor.meta.tags,
        )

        tags.discard(tag)

        return cls.replace_meta(
            descriptor,
            tags=tags,
        )

    @classmethod
    def remove_extra(
        cls,
        descriptor: RequestDescriptor,
        key: str,
    ) -> RequestDescriptor:

        extras = dict(
            descriptor.meta.extras,
        )

        extras.pop(
            key,
            None,
        )

        return cls.replace_meta(
            descriptor,
            extras=extras,
        )