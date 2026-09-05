from __future__ import annotations

from collections.abc import Mapping
from copy import deepcopy
from dataclasses import replace
from typing import Any, Self


from core.merger.mapping import MappingMerger
from core.request.config import RequestConfig
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

    def __init__(
        self,
        descriptor: RequestDescriptor| None = None,
    ) -> None:
        self._descriptor = descriptor

    @property
    def descriptor(self) -> RequestDescriptor:
        descriptor = self._descriptor

        if descriptor is None:
            raise ValueError("Descriptor is not set.")

        return descriptor
    
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
            headers=dict[str, str](headers or {}),
            cookies=dict[str, str](cookies or {}),
            params=dict[str, Any](params or {}),
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
    def from_descriptor(
        cls,
        descriptor: RequestDescriptor,
    ) -> Self:

        return cls(
            cls.clone(descriptor),
        )

    def merge_headers(
        self,
        headers: Mapping[str, str],
        *,
        override: bool = False,
    ) -> Self:

        if not headers:
            return self

        descriptor = self.descriptor

        merger = MappingMerger(
            override=override,
            key_normalizer=str.lower,
        )

        self._descriptor = self.replace(
            descriptor,
            headers=merger.merge(
                descriptor.headers,
                dict(headers),
            ),
        )

        return self


    def merge_cookies(
        self,
        cookies: Mapping[str, str],
        *,
        override: bool = False,
    ) -> Self:

        if not cookies:
            return self

        descriptor = self.descriptor

        merger = MappingMerger(
            override=override,
        )

        self._descriptor = self.replace(
            descriptor,
            cookies=merger.merge(
                descriptor.cookies,
                dict(cookies),
            ),
        )

        return self


    def merge_params(
        self,
        params: Mapping[str, Any],
        *,
        override: bool = False,
    ) -> Self:

        if not params:
            return self

        descriptor = self.descriptor

        merger = MappingMerger(
            override=override,
        )

        self._descriptor = self.replace(
            descriptor,
            params=merger.merge(
                descriptor.params,
                dict(params),
            ),
        )

        return self

    @classmethod
    def from_patch(
        cls,
        *,
        descriptor: RequestDescriptor,
        patch: RequestPatch,
    ) -> RequestDescriptor:

        return (
            cls
            .from_descriptor(descriptor)
            .apply_patch(patch)
            .build()
        )

    def apply_patch(
        self,
        patch: RequestPatch,
    ) -> Self:

        descriptor = self.descriptor

        self._descriptor = self.create(
            url=(
                patch.url
                if patch.url is not None
                else descriptor.url
            ),
            kind=descriptor.kind,
            profile=descriptor.profile,
            method=descriptor.method,
            headers=(
                dict(patch.headers)
                if patch.headers is not None
                else descriptor.headers
            ),
            cookies=(
                dict(patch.cookies)
                if patch.cookies is not None
                else descriptor.cookies
            ),
            params=(
                dict(patch.params)
                if patch.params is not None
                else descriptor.params
            ),
            body=(
                deepcopy(patch.body)
                if patch.has_body()
                else descriptor.body
            ),
            meta=deepcopy(
                descriptor.meta,
            ),
        )

        return self
    # ---------------------------------------------------------
    # utilities
    # ---------------------------------------------------------

    @classmethod
    def clone(
        cls,
        descriptor: RequestDescriptor,
    ) -> RequestDescriptor:
        return replace(
            descriptor,
            headers=dict(descriptor.headers),
            cookies=dict(descriptor.cookies),
            params=dict(descriptor.params),
            body=deepcopy(descriptor.body),
            meta=replace(
                descriptor.meta,
                tags=frozenset(descriptor.meta.tags),
                extras=deepcopy(descriptor.meta.extras),
            ),
        )

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

    def build(self) -> RequestDescriptor:

        return self.descriptor