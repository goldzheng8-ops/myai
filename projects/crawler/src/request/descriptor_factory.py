

from copy import deepcopy
from typing import Any, Mapping

from config.discovery.base import RequestPatch

from enums.http_method import HttpMethod
from enums.request_kind import RequestKind
from runtime.discovery_descriptor import RequestDescriptor
from runtime.request_context import RequestContext
from runtime.request_profile import RequestProfile


class RequestDescriptorFactory:

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
        params: Mapping[str, str] | None = None,
        body: Any = None,
        meta: Mapping[str, Any] | None = None,
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
            meta=dict(meta or {}),
        )

    @classmethod
    def detail(
        cls,
        *,
        url: str,
        profile: RequestProfile,
        method: HttpMethod = HttpMethod.GET,
        headers: Mapping[str, str] | None = None,
        cookies: Mapping[str, str] | None = None,
        params: Mapping[str, str] | None = None,
        body: Any = None,
        meta: Mapping[str, Any] | None = None,
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
            meta=meta

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
        params: Mapping[str, str] | None = None,
        body: Any = None,
        meta: Mapping[str, Any] | None = None,
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
            meta=meta

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
        params: Mapping[str, str] | None = None,
        body: Any = None,
        meta: Mapping[str, Any] | None = None,
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
            meta=meta

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
        params: Mapping[str, str] | None = None,
        body: Any = None,
        meta: Mapping[str, Any] | None = None,
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
            meta=meta

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
        params: Mapping[str, str] | None = None,
        body: Any = None,
        meta: Mapping[str, Any] | None = None,
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
            meta=meta

        )

    @classmethod
    def api_from_patch(
        cls,
        *,
        context: RequestContext,
        patch: RequestPatch,
    ) -> RequestDescriptor:
        return cls.api(
            url=patch.url or context.request.url,
            profile=context.profile,
            params=patch.params,
            body=patch.body,
        )

